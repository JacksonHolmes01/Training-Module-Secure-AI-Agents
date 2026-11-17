# Lesson 7: Closing the Gap, and the Blind Spots

The campaign missed the confused deputy (R7) because its rule, `A7`, is disabled.

## Why a rule ships disabled

`A7` fires when a junior user's session queries customer contact details:

```json
{"id": "A7", "name": "Junior user read customer contacts", "enabled": false,
 "match": {"event": "tool_call", "tool": "query_db", "summary.selects_contact": true, "user": "bob"}, ...}
```

The trouble is that bob, legitimately, handles his own accounts, and looking up a contact he is allowed to see also queries contact details. On a busy system this rule can fire often on normal work. That is **alert fatigue**: a rule that cries wolf gets ignored, and then it is worse than no rule. So it ships off, with a note, for you to decide.

In this lab, Part 3's per-user data access already **stops** bob from seeing other accounts, so the rule would mostly flag his own legitimate lookups. You might leave it off and rely on prevention, or turn it on in a tighter form. Try it on:

```bash
bin/detect.py --enable A7
bin/coverage.py
```

```
R7    Confused deputy    DETECTED    A7
Detection coverage: 7 of 7 attack steps (100%)
```

Full coverage, but now you own the noise. That trade-off, more detection versus more false alarms, is the core judgment of detection engineering. There is no setting that is always right; there is the setting you chose on purpose.

## The blind spots

Even at 100%, be honest about what this covers:

- **It detects attempts the rules were written for.** A new attack shape, one you have not seen, has no rule yet. Detection always trails the attacker
- **It cannot detect what did not happen.** If a prompt injection fails to move the model, there is no tool call, and nothing to see. That is fine when the attack failed, and a problem if you mistake "quiet" for "safe"
- **It watches the agent's tool calls.** An attack that never calls a tool, or that works entirely inside a compromised library, is outside this log's field of view. Other logs (the gateway, the containers, the network) see what this one cannot

A single coverage number, like a single audit score, never tells the whole story. Write it down with what it does not cover.

## Write the report

```bash
bin/coverage.py --report
```

This saves a short findings report under `redteam/`: the steps, what was detected, and what was missed, ready to hand to whoever owns the agent.

Next: [Conclusion](08-conclusion.md)
