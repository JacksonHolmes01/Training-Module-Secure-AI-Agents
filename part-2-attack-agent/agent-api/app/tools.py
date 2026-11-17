"""
tools.py: what the agent can DO.

Each tool has two parts:
  - a SCHEMA: the name, description, and arguments the model sees
  - a FUNCTION: the code that runs when the model asks for that tool

These are written the way many agent tutorials write them: they work, and
they trust the model completely. Part 2 attacks every one of these choices:
  read_file   joins the path onto the workspace folder without checking it
  fetch_url   fetches ANY address, including attacker sites
  send_email  sends to ANY recipient
  query_db    runs whatever SQL the model writes, as one shared login
  plugins     tools loaded from outside servers are trusted as written
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Any, Callable, Dict

import json
import logging

import httpx

from . import db
from .embeddings import embed_texts

WORKSPACE  = os.getenv("WORKSPACE_DIR", "/workspace")
SMTP_HOST  = os.getenv("SMTP_HOST", "mailpit")
SMTP_PORT  = int(os.getenv("SMTP_PORT", "1025"))
MAIL_FROM  = os.getenv("MAIL_FROM", "helpbot@bluebird.example.com")
MAX_TEXT   = int(os.getenv("TOOL_MAX_CHARS", "2000"))
# Extra tools published by other servers (the idea behind MCP and similar
# "tool server" protocols). Comma-separated URLs; each returns a JSON list.
PLUGIN_URLS = [u.strip() for u in os.getenv("PLUGIN_URLS", "").split(",") if u.strip()]

log = logging.getLogger("tools")


def _schema(name: str, description: str, **params: str) -> Dict[str, Any]:
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object",
                       "properties": {p: {"type": "integer" if t == "int" else "string", "description": d}
                                      for p, (t, d) in ((p, v.split(":", 1)) for p, v in params.items())},
                       "required": list(params)}}}


SCHEMAS = [
    _schema("search_docs", "Search the company knowledge base (security policies, procedures, product notes).",
            query="str:what to search for"),
    _schema("read_file", "Read a text file from the team's shared workspace folder.",
            path="str:file path inside the workspace, for example reports/q3-summary.md"),
    _schema("fetch_url", "Fetch a web page and return its text.",
            url="str:the full URL, starting with http:// or https://"),
    _schema("send_email", "Send an email on behalf of the support team.",
            to="str:recipient email address", subject="str:subject line", body="str:message text"),
    _schema("query_db", "Run a SQL query on the customer database. Tables: crm.customers(id, name, email, plan, "
            "account_manager, notes) and crm.tickets(id, customer_id, summary, created_by, created_at).",
            sql="str:one SQL statement"),
    _schema("create_ticket", "Create a support ticket for a customer.",
            customer_id="int:the customer's id", summary="str:a short description of the problem"),
]


def _clip(text: str) -> str:
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + f"\n...[cut at {MAX_TEXT} characters]"


async def search_docs(args: Dict[str, Any], user: str) -> str:
    vec = (await embed_texts([str(args.get("query", ""))]))[0]
    rows = await db.search(vec, 3)
    return _clip("\n\n".join(f"[{r['title']}]\n{r['content']}" for r in rows) or "No documents found.")


async def read_file(args: Dict[str, Any], user: str) -> str:
    path = os.path.join(WORKSPACE, str(args.get("path", "")))
    with open(path, encoding="utf-8", errors="replace") as f:
        return _clip(f.read())


async def fetch_url(args: Dict[str, Any], user: str) -> str:
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        r = await client.get(str(args.get("url", "")))
    return _clip(f"HTTP {r.status_code}\n{r.text}")


async def send_email(args: Dict[str, Any], user: str) -> str:
    msg = EmailMessage()
    msg["From"], msg["To"] = MAIL_FROM, str(args.get("to", ""))
    msg["Subject"] = str(args.get("subject", ""))
    msg.set_content(str(args.get("body", "")))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
        s.send_message(msg)
    return f"Email sent to {msg['To']}."


async def query_db(args: Dict[str, Any], user: str) -> str:
    result = await db.run_sql(str(args.get("sql", "")))
    return _clip(str(result))


async def create_ticket(args: Dict[str, Any], user: str) -> str:
    ticket = await db.create_ticket(int(args.get("customer_id", 0)), str(args.get("summary", "")), user)
    return f"Ticket {ticket} created."


FUNCTIONS: Dict[str, Callable] = {
    "search_docs": search_docs, "read_file": read_file, "fetch_url": fetch_url,
    "send_email": send_email, "query_db": query_db, "create_ticket": create_ticket,
}


# --------------------------------------------------------------------
# Plugin tools
# A tool server publishes a list like:
#   {"tools": [{"name": "...", "description": "...", "parameters": {...},
#               "endpoint": "http://.../run"}]}
# The agent shows each tool's name and description to the model exactly as
# published, and calling the tool POSTs the arguments to its endpoint.
# --------------------------------------------------------------------
_plugins_loaded = False


def _plugin_function(endpoint: str) -> Callable:
    async def call(args: Dict[str, Any], user: str) -> str:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(endpoint, json=args)
        return _clip(r.text)
    return call


async def load_plugins() -> None:
    """Fetch every plugin list once, and add its tools to SCHEMAS and FUNCTIONS."""
    global _plugins_loaded
    if _plugins_loaded:
        return
    _plugins_loaded = True
    for url in PLUGIN_URLS:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                listing = (await client.get(url)).json()
            for t in listing.get("tools", []):
                name = str(t["name"])
                if name in FUNCTIONS:
                    continue  # never let a plugin replace a built-in tool
                SCHEMAS.append({"type": "function", "function": {
                    "name": name, "description": str(t.get("description", "")),
                    "parameters": t.get("parameters") or {"type": "object", "properties": {}}}})
                FUNCTIONS[name] = _plugin_function(str(t["endpoint"]))
                log.info("Loaded plugin tool %s from %s", name, url)
        except Exception as e:
            log.warning("Could not load plugins from %s: %s", url, e)
