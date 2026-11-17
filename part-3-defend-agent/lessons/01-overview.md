# Lesson 1: Defending an Agent

In Part 2 you made HelpBot email your customer list to a stranger, hand data to a malicious tool, read secret files, and serve an intern data he could not have. Every attack used only things the agent was allowed to do.

So the defense is not "make the model smarter" or "write a better prompt." You cannot win by asking the model to please ignore attackers, because the model cannot reliably tell an attacker's text from yours. The defense is to **take away the ability to do harm**, in the code around the model, while leaving the agent able to do its job.

You will add six defenses, one at a time, and measure each one with the exact attack harness from Part 2:

| # | Defense | Attack it stops |
|---|---|---|
| 1 | Confine file paths | Path traversal |
| 2 | Email allowlist | Emailing data to an attacker |
| 3 | Fetch allowlist | Sending data out through a URL |
| 4 | Approved tools only | Tool poisoning |
| 5 | Per-user data access | Confused deputy |
| 6 | Human approval, and spotlighting | Defense in depth |

## The idea behind all of them: least privilege

Every defense here is the same principle applied in a different place: **let each part of the system do only what it needs, and nothing more.**

- A file-reading tool needs the workspace, not the whole disk
- An email tool needs to reach customers and the company, not the whole internet
- The agent needs the tools you chose, not tools a stranger published
- The agent acting for bob needs bob's access, not everyone's

None of these defenses trusts the model to behave. Each one makes the harmful action **impossible**, so it does not matter whether the model was fooled.

## How you turn them on

```bash
bin/defend.sh status            # which defenses are on
bin/defend.sh paths on          # turn one on
bin/defend.sh level 3           # turn on the first 3, in order
bin/defend.sh all on
```

Each change restarts the agent so it takes effect.

Next: [Setup](02-setup.md)
