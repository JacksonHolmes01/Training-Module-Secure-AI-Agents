# Lesson 8: Conclusion

You attacked an AI agent and made it work against its own company:

- **Indirect injection** through a file: the agent emailed the entire customer list, and an internal credential, to an attacker
- **Web-page injection**: a page anyone on the internet can publish made the agent send data out through a URL, or relay the attacker's instructions to a trusted user
- **Tool poisoning**: a partner tool declared a required field, and the agent handed over user and customer data during an ordinary tracking request
- **Path traversal**: a workspace tool read a secret file far outside the workspace
- **Confused deputy**: an intern got data he is not allowed to see, with no attack at all

And one idea tied them together: **the model cannot tell your instructions from an attacker's.** System prompt, user message, document, web page, file, tool description, they are all just text in the same context, and the agent acts on all of it.

## The uncomfortable summary

Every attack used only capabilities the agent was **supposed** to have. Nothing was hacked. No password was guessed. The agent read a file, queried a database, called a tool, sent an email, exactly what it was built to do. The attacker only had to supply the text that decided when.

## What comes next

**Part 3: Defend the Agent.** You will add defenses in layers and measure each one with this same harness:
- an allowlist of which tools the agent may use, and for which user
- argument checks: where email may go, which URLs may be fetched, which paths may be read
- a human approval step before the agent sends email or writes data
- real per-user permissions, so the agent acts with bob's access, not its own

The goal is the same scoreboard you built here, run again after each defense, until the attacks that succeed drop to zero.

---

License: CC BY-SA 4.0. Jackson Holmes
