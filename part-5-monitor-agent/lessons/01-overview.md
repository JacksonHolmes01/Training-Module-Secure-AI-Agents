# Lesson 1: Watching the Agent

Parts 3 and 4 made the agent hard to abuse: guards in the code, a sandbox, least privilege, egress limits. Run the attacks now and most of them are blocked.

But notice how every one of those blocks happened: **quietly.** The agent refused, logged nothing you were watching, and answered the user. If a real attacker were probing your agent right now, trying injection after injection, nobody would know. Defenses that work in silence tell you nothing about who is attacking you, how often, or whether tomorrow's attempt will find a gap.

Monitoring fixes that. The job of this part is to make the agent's actions **visible**: record every tool call and every decision, write rules that recognize the shape of an attack, and prove, with a scored red-team campaign, that a real attack would raise an alarm.

| You will build | With |
|---|---|
| A security log of every tool call and decision | `agent-api/app/seclog.py`, read with `bin/logs.py` |
| Detection rules for the attack signatures | `detections/rules.json`, run with `bin/detect.py` |
| A red-team campaign and a coverage score | `bin/redteam.py`, `bin/coverage.py` |

## Detection is not prevention

Keep the two jobs separate. Parts 3 and 4 **prevent** harm. Part 5 **detects** attempts. You need both: prevention stops the attack that fits your rules, and detection tells you about the attack that is testing them, including the one that will eventually slip through. A blocked attack is still an attack, and you want to know it happened.

Next: [Setup](02-setup.md)
