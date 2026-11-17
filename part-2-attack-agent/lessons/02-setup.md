# Lesson 2: Setup

Part 2 is the Part 1 agent with attack content added: poisoned files, a poisoned web page, and a malicious partner tool. Nothing about the agent's code changed. That is the point: the same agent, attacked.

## Start it

```bash
cd Training-Module-Secure-AI-Agents/part-2-attack-agent
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh          # fast if you did Part 1: same models
bin/ingest_sample.sh        # the normal company knowledge base
bin/smoke_test.sh
```

## What is new

| Added | Where | Attack it enables |
|---|---|---|
| `notes/partner-request.md` | the workspace | Indirect injection: exfiltrate customer data |
| `notes/vendor-email.md` and `notes/integrations.md` | the workspace | Indirect injection: exfiltrate a credential |
| A malicious `track_shipment` tool | served by the outside site at `/tools.json` | Tool poisoning |
| `pricing-update.html` | the outside site | A web-page injection to inspect by hand |

The outside site now also plays an attacker who **collects** what the agent sends: every request it receives is logged, and you read that log with `bin/external_log.sh`.

## The malicious tool is already loaded

Look at `.env`:

```
PLUGIN_URLS=http://partner-news.example/tools.json
```

The team "installed" a shipment-tracking tool from a freight partner by adding its URL. On startup the agent fetches that list and adds its tools, exactly how tool-server protocols like MCP work. You will see what that trust costs in Lesson 6.

## The attack harness

```bash
python3 attacks/run_attacks.py
```

It runs every attack, up to three times each, and reports what really happened. Read the next lessons first to understand each one, then come back and run it.

Next: [Indirect Injection: Stealing Data](03-indirect-injection.md)
