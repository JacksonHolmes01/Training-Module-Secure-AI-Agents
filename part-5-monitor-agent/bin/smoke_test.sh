#!/usr/bin/env bash
# End-to-end check: gateway, users, database, model, and one tool call.
set -euo pipefail
cd "$(dirname "$0")/.."
A="$(grep -E '^ALICE_API_KEY=' .env | cut -d= -f2-)"
U=http://localhost:8088
pass() { echo "  ✔ $1"; }
fail() { echo "  ✘ $1"; exit 1; }
echo "[1/5] gateway up";             [[ "$(curl -s $U/proxy-health)" == "ok" ]] && pass "NGINX is up" || fail "NGINX not reachable"
echo "[2/5] no key is rejected";     [[ "$(curl -s -o /dev/null -w '%{http_code}' $U/health)" == "401" ]] && pass "401" || fail "expected 401"
echo "[3/5] wrong key is rejected";  [[ "$(curl -s -o /dev/null -w '%{http_code}' -H 'X-API-Key: wrong' $U/health)" == "403" ]] && pass "403" || fail "expected 403"
echo "[4/5] database";               curl -s -H "X-API-Key: $A" $U/health | grep -q '"db_ok":true' && pass "db_ok" || fail "database not healthy"
echo "[5/5] the agent uses a tool (can take a minute the first time)"
curl -s -X POST $U/chat -H "X-API-Key: $A" -H "Content-Type: application/json" \
  -d '{"message":"What does our policy say about password resets?"}' | grep -q '"tool":"search_docs"' \
  && pass "agent called search_docs" || fail "agent did not use a tool (did you run bin/pull_models.sh and bin/ingest_sample.sh?)"
echo "All smoke tests passed."
