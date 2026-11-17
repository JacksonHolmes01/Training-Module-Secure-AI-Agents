# Part 1: Build the Agent

A RAG chatbot answers. An **agent** acts. In this part you build **HelpBot**, an agent for a fictional support team, with six real tools: search the knowledge base, read workspace files, fetch web pages, query the customer database, create tickets, and send email. You will see exactly how a model "calls a tool", watch every action in a trace, and find the weak points Part 2 will attack.

Everything runs locally. Sent email lands in a fake inbox, and "the internet" is a small website in a container that records every request it receives.

---

## Lessons (read in order)

1. [From Chatbot to Agent](lessons/01-overview.md)
2. [Setup](lessons/02-setup.md)
3. [The Agent Loop](lessons/03-agent-loop.md)
4. [The Tools](lessons/04-tools.md)
5. [Users and the Gateway](lessons/05-users-and-gateway.md)
6. [Email and the Web](lessons/06-email-and-web.md)
7. [The Database](lessons/07-database.md)
8. [The Chat UI](lessons/08-chat-ui.md)
9. [What Could Go Wrong](lessons/09-what-could-go-wrong.md)
10. [Conclusion](lessons/10-conclusion.md)

---

## Quick start

```bash
bin/setup_secrets.sh
docker compose up -d --build
bin/pull_models.sh
bin/ingest_sample.sh
bin/smoke_test.sh
bin/ask.sh alice "What does our policy say about password resets?"
```

| Address | What |
|---|---|
| http://localhost:7860 | Chat UI (pick alice or bob) |
| http://localhost:8025 | Fake email inbox |
| http://localhost:8088 | The API, behind NGINX |

## Requirements
- Docker with Compose v2, 8 GB of memory for Docker, about 5 GB of free disk
- `python3` and `curl` on your computer

License: code is MIT, lessons are CC BY-SA 4.0. See [README-LICENSE.md](../README-LICENSE.md).
