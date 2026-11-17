# Lesson 9: Conclusion

You took the agent that lost every attack in Part 2 and closed all of them, without making it useless:

- **Confined the tools.** `read_file` stays in its workspace, enforced by resolving the real path
- **Controlled the exits.** Email may only reach the company and its customers; the web tool may only reach an allowlist. Stolen data has nowhere to go
- **Approved the tools.** Only tools you chose run, so a stranger's plugin cannot carry your data out
- **Acted as the user.** Row-level security scopes each query to the person chatting, so an intern cannot reach an enterprise account
- **Added depth.** A human approves the actions that matter, and spotlighting reminds the model which text is data

## The lesson under all of it

Not one of these defenses asked the model to behave. Every one of them made a harmful action **impossible** in the code around the model: the path cannot escape, the email cannot reach an outsider, the tool cannot run, the row cannot be read. That is the only kind of defense you can trust against prompt injection, because the thing you cannot trust is exactly the model's judgment about whose instructions to follow.

Spotlighting, the one defense that *does* lean on the model, came last and on purpose. It helps. It is never the foundation.

## What you still cannot stop here

Two gaps remain, and they are the next two parts:

- **Contain the blast.** The approved tools still run inside the agent's own container, with its network and its filesystem. If an attacker found a way to run code (through a tool that executes things, say), the limits above would not hold it. **Part 4** puts the risky parts in a locked box: no network, read-only, least-privilege, so even a fooled agent is stuck.
- **Know when it happened.** Every block in this part was recorded in the trace, but nobody is watching. **Part 5** turns these events into logs, detection rules, and a red-team campaign, so a real attack raises an alert instead of passing quietly.

---

License: CC BY-SA 4.0. Jackson Holmes
