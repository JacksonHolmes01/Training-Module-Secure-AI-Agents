#!/usr/bin/env bash
# Runs once, when the database is created for the first time.
#
# Two schemas:
#   kb   the knowledge base the agent searches (documents + embeddings)
#   crm  a small customer database the agent can query and add tickets to
#
# Part 1 sets this up the way many agent tutorials do: ONE database login
# for the agent (agent_app), which can read every customer and write tickets
# no matter which human is chatting. Part 3 replaces that with per-user access.
set -euo pipefail

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -v ingest_pw="$(cat /run/secrets/kb_ingest_password)" \
  -v agent_pw="$(cat /run/secrets/agent_app_password)" \
  -v embed_dim="${EMBED_DIM:-768}" <<'SQL'
-- Logins -------------------------------------------------------------
CREATE ROLE kb_ingest LOGIN PASSWORD :'ingest_pw';   -- adds documents
CREATE ROLE agent_app LOGIN PASSWORD :'agent_pw';    -- everything the agent does

REVOKE CONNECT ON DATABASE postgres  FROM PUBLIC;
REVOKE ALL     ON DATABASE agentlab  FROM PUBLIC;
GRANT  CONNECT ON DATABASE agentlab  TO kb_ingest, agent_app;
REVOKE CREATE  ON SCHEMA public FROM PUBLIC;

-- Knowledge base -------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA kb AUTHORIZATION postgres;
CREATE TABLE kb.documents (
  id         bigserial PRIMARY KEY,
  title      text NOT NULL DEFAULT '',
  url        text NOT NULL DEFAULT '',
  source     text NOT NULL DEFAULT '',
  content    text NOT NULL,
  embedding  vector(:embed_dim) NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX documents_embedding_hnsw ON kb.documents USING hnsw (embedding vector_cosine_ops);
GRANT USAGE ON SCHEMA kb TO kb_ingest, agent_app;
GRANT SELECT, INSERT ON kb.documents TO kb_ingest;
GRANT USAGE ON SEQUENCE kb.documents_id_seq TO kb_ingest;
GRANT SELECT ON kb.documents TO agent_app;

-- Customer database ------------------------------------------------------
CREATE SCHEMA crm AUTHORIZATION postgres;
CREATE TABLE crm.customers (
  id              integer PRIMARY KEY,
  name            text NOT NULL,
  email           text NOT NULL,
  plan            text NOT NULL,          -- free, pro, enterprise
  account_manager text NOT NULL,          -- which support agent owns the account
  notes           text NOT NULL DEFAULT ''
);
CREATE TABLE crm.tickets (
  id          bigserial PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES crm.customers(id),
  summary     text NOT NULL,
  created_by  text NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);
GRANT USAGE ON SCHEMA crm TO agent_app;
GRANT SELECT ON crm.customers TO agent_app;
GRANT SELECT, INSERT ON crm.tickets TO agent_app;
GRANT USAGE ON SEQUENCE crm.tickets_id_seq TO agent_app;

-- Sample customers (fictional; every address is on example.com/.org/.net)
INSERT INTO crm.customers (id, name, email, plan, account_manager, notes) VALUES
 (1,  'Harbor Logistics',    'ops@harbor-logistics.example.com',  'enterprise', 'alice', 'Renewal in March. Prefers phone calls.'),
 (2,  'Maple Dental Group',  'it@mapledental.example.org',         'pro',        'alice', 'Asked about SSO last quarter.'),
 (3,  'Northfield Schools',  'helpdesk@northfield.example.net',    'enterprise', 'alice', 'Strict data-retention requirements.'),
 (4,  'Copperline Bikes',    'owner@copperline.example.com',       'free',       'bob',   'Trial user, evaluating the pro plan.'),
 (5,  'Riverside Clinic',    'admin@riverside-clinic.example.org', 'enterprise', 'alice', 'Healthcare customer: handle data carefully.'),
 (6,  'Sunrise Bakery',      'hello@sunrisebakery.example.com',    'free',       'bob',   ''),
 (7,  'Atlas Engineering',   'support@atlas-eng.example.net',      'pro',        'alice', 'Two open tickets about exports.'),
 (8,  'Pinecrest Hotels',    'tech@pinecrest.example.com',         'enterprise', 'alice', 'Billing contact changed in May.'),
 (9,  'Lumen Books',         'team@lumenbooks.example.org',        'pro',        'bob',   ''),
 (10, 'Granite Legal LLP',   'it@granitelegal.example.com',        'enterprise', 'alice', 'Legal hold on all records.');

INSERT INTO crm.tickets (customer_id, summary, created_by) VALUES
 (7, 'CSV export times out for large reports', 'alice'),
 (7, 'Export file names contain spaces',       'alice'),
 (4, 'Question about upgrading to pro',        'bob');
SQL

echo "Database ready: knowledge base, customer database, and agent login."
