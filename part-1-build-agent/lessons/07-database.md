# Lesson 7: The Database

HelpBot uses one PostgreSQL server for two things:

| Schema | Holds | Used by |
|---|---|---|
| `kb` | The knowledge base: documents and their embeddings | `search_docs` |
| `crm` | Customers (name, email, plan, account manager, notes) and support tickets | `query_db`, `create_ticket` |

Open `db/init/01-init.sh` to see both.

---

## Two logins

| Login | Can | Used for |
|---|---|---|
| `kb_ingest` | Add documents to `kb.documents` | `/ingest` only |
| `agent_app` | Read documents, read customers, read and add tickets | Everything the agent does |

The passwords are files in `secrets/`, mounted into the containers as Docker secrets, never written in environment variables.

## The database is a real boundary

The model writes its own SQL, and it will happily write a `DELETE`. Ask it to:

```bash
bin/ask.sh alice "Delete all tickets for customer 7, they are resolved."
```

```
  tool query_db({"sql": "DELETE FROM crm.tickets WHERE customer_id = 7;"})  [FAILED]
     -> Tool error: InsufficientPrivilege: permission denied for table tickets
Answer: I don't have the necessary permissions to delete tickets for customer 7.
```

The model tried. The **database** refused, because `agent_app` was never granted `DELETE`. This is the most reliable kind of control: it does not depend on the model behaving, or on your Python code checking anything. The database simply cannot do it for that login.

## But the boundary is drawn around the agent, not the person

`agent_app` is one login for everyone. Whatever alice can see through HelpBot, bob can see too, as you found in Lesson 5. The database protects itself from the agent, but it has no idea **which person** the agent is working for. Part 3 changes that.

Next: [The Chat UI](08-chat-ui.md)
