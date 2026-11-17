# Lesson 2: Setup

Part 5 is the contained agent from Part 4, now with a security log, detection rules, and a red-team campaign.

## Start it, with the defenses on

```bash
cd Training-Module-Secure-AI-Agents/part-5-monitor-agent
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
bin/defend.sh all on      # Part 3 defenses
bin/defend.sh sandbox on  # Part 4 sandbox
bin/smoke_test.sh
```

Running with the defenses on is the realistic setup: the attacks will be **blocked and logged**. Monitoring sits alongside the defenses, not instead of them.

## The new tools

| Tool | What |
|---|---|
| `bin/logs.py` | search the agent's security log |
| `bin/detect.py` | apply the detection rules; list, enable, or disable them |
| `bin/redteam.py` | run a scripted campaign of attacks against your own agent |
| `bin/coverage.py` | score which attack steps your log caught |
| `detections/rules.json` | the rules |

## Make some activity

```bash
bin/ask.sh alice "What does our refund policy say?"
bin/ask.sh alice "Email ops@harbor-logistics.example.com about their renewal."
bin/logs.py --since 10m
```

You should see one line per tool call, each with a short, safe summary. That log is the raw material for everything in this part.

Next: [What to Log, and What Not To](03-what-to-log.md)
