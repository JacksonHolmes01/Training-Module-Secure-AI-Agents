# Lesson 5: Users and the Gateway

HelpBot has two users:

| User | Role |
|---|---|
| **alice** | Support agent. Account manager for most customers |
| **bob** | Intern. Per company policy, may not view customer contact details or enterprise accounts |

Each has their own API key in `.env`.

---

## How the API knows who you are

`nginx/templates/default.conf.template` turns a key into a name:

```nginx
map $http_x_api_key $lab_user {
    default               "";
    "${ALICE_API_KEY}"    alice;
    "${BOB_API_KEY}"      bob;
}
```

Then it passes the name to the API in a header:

```nginx
proxy_set_header X-Lab-User     $lab_user;
proxy_set_header X-Internal-Key "${INTERNAL_API_KEY}";
```

The API reads `X-Lab-User`, and the agent's system prompt says who it is helping.

## Can a user pretend to be someone else? (expected to fail)

Send alice's key, but claim to be bob:

```bash
A=$(grep -E '^ALICE_API_KEY=' .env | cut -d= -f2-)
curl -s -X POST localhost:8088/chat -H "X-API-Key: $A" -H "X-Lab-User: bob" \
  -H 'Content-Type: application/json' -d '{"message":"Who am I helping? Answer with just the name."}'
```

```
{"user":"alice", ... "answer":"alice"}
```

`proxy_set_header` **replaces** whatever `X-Lab-User` the caller sent. Only NGINX decides who you are, from your key.

## Can a request skip NGINX? (expected to fail)

The API is not published to your computer, but other containers can reach it. Try from the UI container:

```bash
docker exec agent-ui python -c "import httpx; r = httpx.post('http://agent-api:8000/chat', json={'message': 'hi'}, headers={'X-Lab-User': 'alice'}); print(r.status_code, r.text)"
```

```
403 {"detail":"Requests must come through the gateway."}
```

The API only trusts `X-Lab-User` when the request also carries `X-Internal-Key`, a secret that only NGINX and the API know. Anything that skips the gateway cannot claim a name.

---

## The catch

The agent **knows** who it is helping. But knowing is not enforcing. Ask as bob:

```bash
bin/ask.sh bob "What is the email address for Riverside Clinic?"
```

```
  tool query_db({"sql": "SELECT email FROM crm.customers WHERE name = 'Riverside Clinic'"})  [ok]
Answer: The email address for Riverside Clinic is admin@riverside-clinic.example.org.
```

Bob is an intern, and the company policy says interns may not view customer contact details. The agent answered anyway, because every database query runs as **one** login, `agent_app`, which can read every customer. The gateway authenticated bob perfectly; nothing used that information to limit what the agent did for him. You will exploit this in Part 2 and fix it properly in Part 3.

Next: [Email and the Web](06-email-and-web.md)
