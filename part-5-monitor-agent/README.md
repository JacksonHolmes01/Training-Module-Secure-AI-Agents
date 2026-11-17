# Part 5: Monitor the Agent

Parts 3 and 4 made the agent hard to abuse, but every block happened in silence. This part makes the agent's actions **visible**: a security log of every tool call, detection rules for the attack signatures, and a red-team campaign scored for coverage, so a real attack raises an alarm instead of passing quietly.

Prevention and detection are different jobs. The defenses stop the attack; monitoring tells you it was tried.

---

## Lessons (read in order)

1. [Watching the Agent](lessons/01-overview.md)
2. [Setup](lessons/02-setup.md)
3. [What to Log, and What Not To](lessons/03-what-to-log.md)
4. [Searching the Log](lessons/04-searching.md)
5. [Detection Rules](lessons/05-detection-rules.md)
6. [The Red-Team Campaign](lessons/06-red-team.md)
7. [Closing the Gap, and the Blind Spots](lessons/07-gaps.md)
8. [Conclusion](lessons/08-conclusion.md)

---

## Quick start

```bash
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
bin/defend.sh all on && bin/defend.sh sandbox on

bin/redteam.py           # attack your own agent, with the defenses on
bin/coverage.py          # score which attempts your log caught
```

| Command | What |
|---|---|
| `bin/logs.py` | search the security log (`--tool`, `--decision`, `--user`, `--summary`) |
| `bin/detect.py` | run the rules (`--rules`, `--enable A7`, `--disable A7`) |
| `bin/redteam.py` | run the scripted attack campaign |
| `bin/coverage.py` | score detection coverage; `--report` writes a findings report |

## Requirements
- Part 4 completed (Part 5 reuses its models)
- Docker with Compose v2, 8 GB of memory for Docker

License: code is MIT, lessons are CC BY-SA 4.0. See [README-LICENSE.md](../README-LICENSE.md).
