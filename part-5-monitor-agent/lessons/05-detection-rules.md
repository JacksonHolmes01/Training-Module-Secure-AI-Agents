# Lesson 5: Detection Rules

A detection rule turns "I would notice that if I looked" into "the system notices it for me." Open `detections/rules.json`. Each rule matches a kind of event and fires an alert:

```json
{"id": "A1", "name": "Email to an outside address", "severity": "high",
 "match": {"event": "tool_call", "tool": "send_email", "summary.external": true},
 "group_by": "user", "threshold": 1, "window_s": 5,
 "why": "The agent tried to email a domain outside the company. The signature of data exfiltration by email.",
 "response": "Confirm no customer data left, and look at what the agent was asked to do just before."}
```

- **match**: which events this rule cares about. A dotted key like `summary.external` reaches inside the summary
- **threshold / window_s**: fire when this many matching events arrive from one `group_by` (here, one user) within this many seconds. After firing, the rule stays quiet for one window, so a burst makes one alert, not a hundred
- **why / response**: what the alert means and what to do, written for whoever reads it at 3am

## The rules

```bash
bin/detect.py --rules
```

```
  A1  on   high      Email to an outside address
  A2  on   medium    Tool call blocked by policy
  A3  on   high      Unapproved (outside) tool used
  A4  on   high      File path left the workspace
  A5  on   medium    Agent ran code
  A6  on   medium    Burst of tool calls in one chat
  A7  off  high      Junior user read customer contacts
  A8  on   high      Blocked web fetch
```

Each one is the signature of an attack you carried out in Part 2: A1 and A8 for exfiltration, A3 for tool poisoning, A4 for path traversal, A7 for the confused deputy. One (`A7`) starts **off**; you will see why in Lesson 7.

## Run them

```bash
bin/detect.py --since 15m
```

```
03:34:16  HIGH   A1  Email to an outside address  (user=alice, x1)
     why: The agent tried to email a domain outside the company...
03:34:30  HIGH   A3  Unapproved (outside) tool used  (user=alice, x1)
03:34:35  HIGH   A4  File path left the workspace  (user=alice, x1)
```

The rules read the same log you searched by hand, and surface the attacks on their own. But how do you know they catch everything they should? You attack yourself and keep score.

Next: [The Red-Team Campaign](06-red-team.md)
