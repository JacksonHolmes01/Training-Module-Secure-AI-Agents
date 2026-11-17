# Lesson 2: Setup

Part 4 is the Part 3 agent (defenses and all) plus a code tool, a sandbox container, a hardening overlay, and an audit. It starts uncontained, so you can see each containment layer make a difference.

## Start it

```bash
cd Training-Module-Secure-AI-Agents/part-4-contain-agent
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
bin/smoke_test.sh
```

Ten containers come up this time. The new ones:

| Container | What it is |
|---|---|
| `agent-sandbox` | A locked-down box that runs the agent's code snippets |
| `agent-sandbox-perms` | A one-shot helper that prepares the sandbox's shared folder, then exits |

## What is new in the code

| File | What it adds |
|---|---|
| `agent-api/app/code_tool.py` | The `run_python` tool, and its two modes (in-process, or sandboxed) |
| `sandbox/runner.py` + `sandbox/Dockerfile` | The sandbox: runs code with no network, read-only, non-root, limited |
| `hardening/harden.yml`, `bin/harden.sh` | Least-privilege settings for the containers |
| `bin/audit.py` | Scores every container on a hardening checklist |
| `bin/attacker_demo.sh` | Pretends an attacker is inside the agent container |
| `bin/egress.sh` | Demonstrates cutting the agent off from an untrusted network |

Next: [The Most Dangerous Tool](03-code-tool.md)
