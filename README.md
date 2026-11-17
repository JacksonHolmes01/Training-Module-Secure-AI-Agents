# Secure AI Agents: A Hands-On Training Series

Learn to build AI **agents** that are secure: models that do not just answer, but act, by reading files, fetching web pages, querying databases, and sending email.

An agent turns a prompt injection from a bad answer into a real action. This series shows you that first-hand, then teaches you to defend, contain, and monitor an agent, measuring every control instead of trusting it.

It is written for beginners. Everything runs on your own computer with Docker, using a small local model. No cloud account or API key is needed, and nothing leaves your machine: email goes to a fake inbox, and "the internet" is a container that records every request.

---

## The series

| Part | Folder | What you do | Status |
|---|---|---|---|
| 1 | [part-1-build-agent](part-1-build-agent/README.md) | Build HelpBot, an agent with six tools, and see exactly how a model calls tools | Available |
| 2 | [part-2-attack-agent](part-2-attack-agent/README.md) | Make the agent email data out, hand data to a malicious tool, read files it must not, and serve a user more than they may see | Available |
| 3 | [part-3-defend-agent](part-3-defend-agent/README.md) | Confine tools, control the exits, approve tools, act as the user: six defenses, each measured until the attacks stop | Available |
| 4 | [part-4-contain-agent](part-4-contain-agent/README.md) | A sandbox for the code tool, least-privilege containers with an audit, and network egress control: contain the blast radius | Available |
| 5 | [part-5-monitor-agent](part-5-monitor-agent/README.md) | A security log of every tool call, detection rules for the attack signatures, and a red-team campaign scored for coverage | Available |

Do the parts in order. Each one builds on the last. All five parts are available.

---

## Requirements

- macOS, Linux, or Windows with WSL 2
- Docker with Compose v2, 8 GB of memory for Docker, about 5 GB of free disk
- No prior AI, agent, or Docker experience

## Get started

```bash
git clone https://github.com/JacksonHolmes01/Training-Module-Secure-AI-Agents.git
cd Training-Module-Secure-AI-Agents/part-1-build-agent
```

Then open [Part 1](part-1-build-agent/README.md).

---

## Related training modules

Secure the database and the chatbot first, with any of these:

- [Secure AI with pgvector](https://github.com/JacksonHolmes01/Training-Module-Secure-AI-pgvector)
- [Secure AI with Chroma](https://github.com/JacksonHolmes01/Training-Module-Secure-AI-Chroma)
- [Production-Grade RAG Infrastructure: Weaviate](https://github.com/JacksonHolmes01/Training-Module-Production-Grade-RAG-Infrastructure-Weaviate)
- [Production-Grade RAG Infrastructure: Qdrant](https://github.com/JacksonHolmes01/Training-Module-Production-Grade-RAG-Infrastructure-Qdrant)
- [Production-Grade RAG Infrastructure: Milvus](https://github.com/JacksonHolmes01/Training-Module-Production-Grade-RAG-Infrastructure-Milvus)

---

## License

Code and configuration are **MIT**. Lessons and documentation are **CC BY-SA 4.0**. See [README-LICENSE.md](README-LICENSE.md).
