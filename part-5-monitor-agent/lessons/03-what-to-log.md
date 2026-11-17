# Lesson 3: What to Log, and What Not To

Open `agent-api/app/seclog.py`. Every tool call the agent makes becomes one JSON line:

```json
{"event":"tool_call","time":"...","user":"alice","tool":"send_email",
 "decision":"blocked","summary":{"to_domain":"evil.example","external":true},
 "reason":"email to 'sync@evil.example' is not allowed: ..."}
```

It records **who** acted, **what** tool, the **decision** (ok, blocked, or error), and a short **summary**. That is enough to recognize an attack. What it does **not** record is the content: not the email body, not the customer rows, not the file contents, not the secret.

## Prove the log holds no secrets

Run an attack that tries to steal a credential, then search the whole log for that credential:

```bash
bin/ask.sh alice "Please action the forwarded note in notes/vendor-email.md"
docker compose logs --no-color agent-api | grep -c "FF-LIVE-9c2b4a7e13d04f8a"
```

```
0
```

The agent blocked the exfiltration, logged that an email was headed to an outside domain, and the secret itself never touched the log.

## Why this matters

A security log is read by many people and kept for a long time. If it contained the data you are protecting, it would become a second, less-guarded copy of exactly what an attacker wants. So `seclog.py` logs **metadata and decisions**, never content:

| Tool | Logged | Not logged |
|---|---|---|
| `send_email` | recipient domain, whether it is external | the subject, the body |
| `query_db` | whether the query selects contact details, how it was decided | the rows, the SQL values |
| `read_file` | whether the path escaped the workspace | the file contents |
| `run_python` | that code ran | the code, its output |
| any tool | the decision and the reason | the arguments' sensitive values |

> **The rule.** Log what happened and why, enough to investigate, and nothing an attacker would be glad to find in your logs. This is the same discipline as the database series' Part 5, now applied to an agent's actions instead of a database's requests.

Next: [Searching the Log](04-searching.md)
