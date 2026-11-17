# Lesson 1: Why Agents Are Different to Attack

In the prompt injection series, a successful attack produced a bad **answer**: a leaked secret in text, a wrong instruction followed. Annoying, but the damage stopped at words on a screen.

An agent has tools. When you make an agent follow an attacker's instructions, it does not just say something wrong. It **emails your customer list to a stranger**, reads a file it should never touch, or hands your data to an outside server, all while telling you, truthfully as far as it knows, that it helped you.

In this part you attack HelpBot from Part 1. You will:

| Attack | What the agent is tricked into doing |
|---|---|
| Indirect injection (customer data) | Email the entire customer list to an attacker |
| Indirect injection (secret) | Read an internal credential and email it out |
| Tool poisoning | Hand user and customer data to a malicious tool's server |
| Path traversal | Read a secret file outside its workspace |
| Confused deputy | Give an intern data he is not allowed to see |

Every attack is checked by **evidence**, not by the agent's answer: the fake inbox, the attacker's server log, and the trace.

---

## The one idea behind every attack

In Part 1, Lesson 3, you saw that a tool call is just text the model writes, and your code decides whether to run it. Here is the other half:

**The model cannot tell your instructions from everybody else's.**

The system prompt, the user's message, a document from the knowledge base, a web page, a file, even a tool's description, all arrive as the same thing: text in the model's context. If an attacker can get text in front of the model, the attacker can give the agent instructions. And the agent can act.

> **Ethics note.** These techniques are for defending systems you own or are authorized to test. Everything here runs against your own local lab. Do not point these attacks at anyone else.

Next: [Setup](02-setup.md)
