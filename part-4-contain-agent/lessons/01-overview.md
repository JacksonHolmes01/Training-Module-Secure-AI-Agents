# Lesson 1: Containing the Blast Radius

Part 3 defended the agent in its **code**: path checks, email and fetch allowlists, approved tools, per-user data. Those are the right first move, and they work. But every one of them lives inside the agent process, and they all share one assumption: the guard code runs, and runs correctly.

Containment asks the harder question: **what if it doesn't?** What if a guard has a bug, a new tool slips past review, or a library the agent uses has a flaw that lets an attacker run code inside the container? Good security does not bet everything on one layer. It limits how much any single failure can cost.

That limit is built in the **infrastructure** around the agent, not in its prompt or its Python:

| Containment | Limits |
|---|---|
| A code sandbox | What the agent's code tool can touch: no network, no secrets, no disk |
| Least-privilege containers | What an attacker who lands in a container can do |
| Network egress control | Where the agent can send data, even if every code guard failed |

The theme: assume a layer will fail, and make sure the failure is survivable.

## The most dangerous capability

This part adds one new tool, `run_python`, because agents increasingly run code: to do math, parse data, transform a file. "Run code" is the most powerful thing you can hand an agent, because it is really "do anything this process can do." You will see exactly how dangerous that is, and then put it in a box.

Next: [Setup](02-setup.md)
