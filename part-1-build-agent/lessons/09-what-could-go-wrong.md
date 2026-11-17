# Lesson 9: What Could Go Wrong

HelpBot works. It is also built the way many agent tutorials build agents, and you have already seen hints of trouble. Here is every weak point Part 2 will attack, and where it lives in the code.

| # | Weak point | Where | What an attacker can do |
|---|---|---|---|
| 1 | The agent obeys instructions found **inside** documents and web pages | `agent.py`: tool results go straight back to the model | Plant instructions in a page or document, and the agent follows them |
| 2 | `send_email` sends to **any** address | `tools.py` | Make the agent email data to an outside address |
| 3 | `fetch_url` fetches **any** address | `tools.py` | Make the agent send data out inside a web address, or read attacker pages |
| 4 | `read_file` joins the path onto `/workspace` without checking it | `tools.py` | Ask for `../run/secrets/...` and read files outside the workspace |
| 5 | One database login for everyone | `db.py`, `01-init.sh` | Get the agent to show bob what only alice may see |
| 6 | Tool descriptions are trusted as written | `tools.py` schemas | A malicious tool's description becomes an instruction |
| 7 | Nothing asks a human before acting | `agent.py` | Emails and tickets happen with no review |

Look back at Lesson 5: bob asked for a customer's email and got it. That was weak point 5, with no attack needed.

---

## A quick look at weak point 4

```bash
bin/ask.sh alice "Read the file ../etc/hostname"
```

Look at the trace. The path left the workspace folder.

You will do much worse in Part 2.

Next: [Conclusion](10-conclusion.md)
