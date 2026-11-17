# Lesson 2: Setup

## Requirements

- Docker with Compose v2
- 8 GB of memory for Docker, about 5 GB of free disk
- `python3` and `curl` on your computer (standard on macOS and Linux)

## Step 1: Get the lab

```bash
git clone https://github.com/JacksonHolmes01/Training-Module-Secure-AI-Agents.git
cd Training-Module-Secure-AI-Agents/part-1-build-agent
```

## Step 2: Secrets

```bash
bin/setup_secrets.sh
```

This creates:
- database passwords in `secrets/` (one per database login)
- an API key for **alice** and one for **bob** in `.env`
- an internal key that only NGINX and the API share (Lesson 5)

Both `secrets/` and `.env` are ignored by git.

## Step 3: Start everything

```bash
docker compose up -d --build
docker compose ps
```

Nine containers start. Wait until `agent-api` and `agent-db` show `(healthy)`.

## Step 4: Download the models

```bash
bin/pull_models.sh
```

About 2.2 GB the first time: `qwen2.5:3b` (the model that decides which tools to call) and `nomic-embed-text` (for searching the knowledge base). Parts 2 to 5 reuse the same download.

> **Why qwen2.5:3b?** Small models differ a lot at tool calling. Testing this lab, `qwen2.5:3b` picked the right tool with the right arguments 8 times out of 8 and answered in about a second. `llama3.2:3b` managed 5 of 8: asked "what is 12 times 7?", it tried to fetch a web page.

## Step 5: Load the knowledge base

```bash
bin/ingest_sample.sh
```

```
Total: 10  Success: 10  Failed: 0
```

Ten company documents: the password reset procedure, the customer data policy, the intern guidelines, and more.

## Step 6: Check everything works

```bash
bin/smoke_test.sh
```

```
[1/5] gateway up
  ✔ NGINX is up
[2/5] no key is rejected
  ✔ 401
[3/5] wrong key is rejected
  ✔ 403
[4/5] database
  ✔ db_ok
[5/5] the agent uses a tool (can take a minute the first time)
  ✔ agent called search_docs
All smoke tests passed.
```

Next: [The Agent Loop](03-agent-loop.md)
