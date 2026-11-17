# Part 2: Attack the Agent

The agent from Part 1 works. In this part you attack it, and watch it email your customer list to a stranger, hand data to a malicious tool, read secret files, and serve an intern data he may not see. Every attack is checked by **evidence** (the fake inbox, the attacker's server log, the trace), never by the agent's reassuring answer.

Nothing about the agent's code changed from Part 1. The same agent, attacked.

---

## Lessons (read in order)

1. [Why Agents Are Different to Attack](lessons/01-overview.md)
2. [Setup](lessons/02-setup.md)
3. [Indirect Injection: Stealing Data](lessons/03-indirect-injection.md)
4. [Indirect Injection: From a Web Page](lessons/04-web-injection.md)
5. [Tool Poisoning](lessons/05-tool-poisoning.md)
6. [Path Traversal and the Confused Deputy](lessons/06-traversal-and-deputy.md)
7. [What the Agent's Answer Hides](lessons/07-measuring.md)
8. [Conclusion](lessons/08-conclusion.md)

---

## Quick start

```bash
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
python3 attacks/run_attacks.py
```

| Address | What |
|---|---|
| http://localhost:8025 | The fake inbox: see what the agent emailed out |
| http://localhost:7860 | Chat UI (alice or bob) |

Watch the data leave: `bin/inbox.sh` (emails) and `bin/external_log.sh` (what reached the attacker's server).

## Requirements
- Part 1 completed (Part 2 reuses its models)
- Docker with Compose v2, 8 GB of memory for Docker

> **Ethics note.** These techniques are for defending systems you own or are authorized to test. Everything here runs against your own local lab.

License: code is MIT, lessons are CC BY-SA 4.0. See [README-LICENSE.md](../README-LICENSE.md).
