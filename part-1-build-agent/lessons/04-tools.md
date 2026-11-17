# Lesson 4: The Tools

Open `agent-api/app/tools.py`. Every tool has two halves:

| Half | What it is | Who sees it |
|---|---|---|
| **Schema** | The tool's name, description, and arguments | The model |
| **Function** | The Python code that actually runs | Only your server |

```python
_schema("send_email", "Send an email on behalf of the support team.",
        to="str:recipient email address", subject="str:subject line", body="str:message text"),
```

```python
async def send_email(args, user):
    msg = EmailMessage()
    msg["From"], msg["To"] = MAIL_FROM, str(args.get("to", ""))
    ...
```

---

## Try every tool

Run each of these as alice and read the trace each time.

### search_docs: the knowledge base

```bash
bin/ask.sh alice "What does our policy say about refunds over 1000 dollars?"
```

### read_file: the team's shared folder

```bash
bin/ask.sh alice "What is in reports/q3-summary.md?"
```

```
  tool read_file({"path": "reports/q3-summary.md"})  [ok]
     -> # Q3 support summary  - Tickets closed: 1,284 (up 9% from Q2) ...
```

The `workspace/` folder in this lab is mounted into the agent's container, read-only, as `/workspace`.

### fetch_url: web pages

```bash
bin/ask.sh alice "Summarize http://intranet.local/holidays.html"
bin/ask.sh alice "What's the latest shipping update from http://partner-news.example/shipping-update ?"
```

```
  tool fetch_url({"url": "http://partner-news.example/shipping-update"})  [ok]
Answer: The carrier delays on the east coast are expected to ease by Friday. Ground shipments from the Denver hub are running one day behind schedule.
```

### query_db: the customer database

```bash
bin/ask.sh alice "How many customers are on the enterprise plan?"
```

```
  tool query_db({"sql": "SELECT COUNT(*) FROM crm.customers WHERE plan = 'enterprise'"})  [ok]
Answer: There are 5 customers on the enterprise plan.
```

The model wrote that SQL itself, from the table description in the tool's schema.

### create_ticket: a write action

```bash
bin/ask.sh alice "Open a ticket for customer 2: SSO login loops back to the sign-in page."
```

```
  tool create_ticket({"customer_id": 2, "summary": "SSO login loops back to the sign-in page"})  [ok]
```

### send_email: an action with consequences

```bash
bin/ask.sh alice "Email ops@harbor-logistics.example.com to say their export fix ships in Q4."
bin/inbox.sh
```

```
1 message(s). Full text: http://localhost:8025
  to ops@harbor-logistics.example.com       Export fix ships in Q4    The export fix you requested will be available in the fourth...
```

Open **http://localhost:8025** to read it. That is Mailpit, a fake mail server: the agent really sent an email, but it can never leave your computer.

### No tool at all

```bash
bin/ask.sh alice "What is 12 times 7?"
```

```
User: alice   (1 model calls, 0.8s)
Answer: 12 times 7 is 84.
```

A good agent uses tools when they help, not every time.

---

## Tools are capabilities

Count what HelpBot can now do on its own: read files, reach other websites, read and write the customer database, and send email to anyone. Each tool is a **capability**, and the model decides when to use it. The question for the rest of this series is: **who else can make the model decide?**

Next: [Users and the Gateway](05-users-and-gateway.md)
