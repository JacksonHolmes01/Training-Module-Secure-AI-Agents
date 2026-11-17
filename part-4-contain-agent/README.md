# Part 4: Contain the Agent

Part 3 defended the agent in its code. Part 4 assumes that code can fail, and limits the damage with **infrastructure**: a sandbox for the agent's code tool, least privilege for every container, and network egress control.

The theme is defense in depth: assume each layer will sometimes fail, and make the failure survivable.

---

## Lessons (read in order)

1. [Containing the Blast Radius](lessons/01-overview.md)
2. [Setup](lessons/02-setup.md)
3. [The Most Dangerous Tool](lessons/03-code-tool.md)
4. [The Sandbox](lessons/04-sandbox.md)
5. [Least Privilege for Every Container](lessons/05-least-privilege.md)
6. [What Hardening Cannot Fix](lessons/06-egress.md)
7. [Containment Review](lessons/07-review.md)
8. [Conclusion](lessons/08-conclusion.md)

---

## Quick start

```bash
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh

bin/defend.sh sandbox on     # run the code tool in the no-network sandbox
python3 bin/audit.py         # score the containers
bin/harden.sh on             # apply least privilege, then re-audit
bin/attacker_demo.sh         # what an attacker inside the agent container can do
bin/egress.sh test           # can the agent reach the attacker's network?
```

| Command | What |
|---|---|
| `bin/defend.sh sandbox on\|off` | run the code tool in the sandbox, or in-process |
| `bin/harden.sh on\|off` | apply or remove the container hardening overlay |
| `bin/audit.py` | hardening scorecard for every container |
| `bin/attacker_demo.sh` | run commands as an attacker inside the agent container |
| `bin/egress.sh test\|on\|off` | demonstrate network egress control |

## Requirements
- Part 3 completed (Part 4 reuses its models)
- Docker with Compose v2, 8 GB of memory for Docker

License: code is MIT, lessons are CC BY-SA 4.0. See [README-LICENSE.md](../README-LICENSE.md).
