# Lesson 1: From Chatbot to Agent

A RAG chatbot **answers**. It retrieves documents and writes a reply. Whatever it says, it cannot change anything.

An **agent** **acts**. It is given tools (read a file, fetch a web page, query a database, send an email) and it decides, on its own, which tools to call and with what arguments. The model is no longer just writing text for a person to read. Its words become actions.

That is what makes agents useful, and what makes them dangerous. Every prompt injection trick from the other series still works on an agent, but now a successful injection does not just produce a bad answer. It sends an email, reads a file, or changes a record.

---

## What you will build

**HelpBot**, an agent for the support team at a fictional company, Bluebird Supply Co. It runs entirely on your computer:

```
 you (alice or bob)
      |
   NGINX gateway  ---- turns your API key into your user name
      |
   agent-api  ---- the agent loop (FastAPI)
      |   \
      |    +-- Ollama: qwen2.5:3b decides which tools to call
      |
      +-- search_docs   -> knowledge base (PostgreSQL + pgvector)
      +-- query_db      -> customer database (PostgreSQL)
      +-- create_ticket -> customer database
      +-- read_file     -> the team's shared workspace folder
      +-- fetch_url     -> the company intranet, or the outside internet
      +-- send_email    -> Mailpit, a fake mail server with a web inbox
```

Nothing leaves your computer. Every email lands in a fake inbox you can open in your browser, and "the internet" is a small website in a container that records every request it receives.

---

## The series

| Part | You will |
|---|---|
| **1 (this part)** | Build the agent and understand exactly how it calls tools |
| 2 | Attack it: make it email data out, read files it should not, and act for people who are not allowed |
| 3 | Defend it in layers, and measure what each layer stops |
| 4 | Contain it, so even a fooled agent cannot reach what it must not |
| 5 | Monitor it: an audit log of every action, detection rules, and a red-team campaign |

---

## Built the way many tutorials build agents

Part 1 builds HelpBot the way a typical agent tutorial does: it works, and it trusts the model. That is deliberate. You cannot defend against attacks you have never seen succeed, so Part 2 needs a realistic target. Lesson 9 lists the weak points, and you will exploit each one in Part 2.

Next: [Setup](02-setup.md)
