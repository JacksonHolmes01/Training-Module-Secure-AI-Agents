# Lesson 2: Setup

Part 3 is the Part 2 agent, attacks and all, with the defenses added but switched **off**. So it starts exactly as vulnerable as Part 2, and you turn the defenses on and watch the attacks stop.

## Start it

```bash
cd Training-Module-Secure-AI-Agents/part-3-defend-agent
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
bin/smoke_test.sh
```

## Confirm the defenses are all off

```bash
bin/defend.sh status
```

```
  DEFEND_PATHS=false
  DEFEND_EMAIL=false
  DEFEND_URL=false
  DEFEND_TOOLS=false
  DEFEND_DATA=false
  DEFEND_APPROVAL=false
  DEFEND_SPOTLIGHT=false
```

## Confirm the attacks still work

```bash
python3 attacks/run_attacks.py
```

You should see the same picture as Part 2: the data-theft attacks succeed. If they do, your baseline is ready.

## What is new in the code

| File | What it adds |
|---|---|
| `agent-api/app/guards.py` | Every defense, each behind an on/off switch |
| `bin/defend.sh` | Turns defenses on and off and restarts the agent |
| `bin/scoreboard.sh` | Runs the attacks after each defense, so you see the progression |
| `db/init/01-init.sh` | Row-level security on the customer table, for Defense 4 |

Open `guards.py` now and skim it. Every defense is a short function that either allows a tool call or raises `Blocked` with a reason. Read on to turn them on.

Next: [Defense 1: Confine the Tools](03-confine-paths.md)
