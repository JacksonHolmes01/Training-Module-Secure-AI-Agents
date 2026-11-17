# Part 3: Defend the Agent

The agent lost every attack in Part 2. Here you defend it, in six layers, and **measure** each one with the same attack harness. By the end, every Part 2 attack is stopped and the agent still does its job.

The one idea: you cannot ask the model to behave, because it cannot tell an attacker's instructions from yours. So each defense makes a harmful action **impossible** in the code around the model, and leaves the useful ones alone.

---

## Lessons (read in order)

1. [Defending an Agent](lessons/01-overview.md)
2. [Setup](lessons/02-setup.md)
3. [Confine the Tools](lessons/03-confine-paths.md)
4. [Control Where Data Can Go](lessons/04-control-egress.md)
5. [Only Run Tools You Trust](lessons/05-approved-tools.md)
6. [Act as the User, Not as the Agent](lessons/06-per-user-data.md)
7. [A Human in the Loop, and Spotlighting](lessons/07-approval-and-spotlight.md)
8. [The Scoreboard](lessons/08-scoreboard.md)
9. [Conclusion](lessons/09-conclusion.md)

---

## Quick start

```bash
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
python3 attacks/run_attacks.py     # baseline: attacks succeed, as in Part 2
bin/scoreboard.sh                  # turn on defenses one at a time, watch them stop
```

| Command | What |
|---|---|
| `bin/defend.sh status` | which defenses are on |
| `bin/defend.sh <name> on` | turn one on (paths, email, url, tools, data, approval, spotlight) |
| `bin/defend.sh level N` | turn on the first N, in lesson order |
| `bin/scoreboard.sh` | attacks after each defense, the whole progression |

## Requirements
- Part 2 completed (Part 3 reuses its models)
- Docker with Compose v2, 8 GB of memory for Docker

License: code is MIT, lessons are CC BY-SA 4.0. See [README-LICENSE.md](../README-LICENSE.md).
