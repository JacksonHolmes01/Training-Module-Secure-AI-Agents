"""
seclog.py: the agent's security log.

Every tool call the agent makes, and every chat, is written as one JSON line
to the container's output (so `docker compose logs` captures it). These lines
are what Part 5 searches, writes detection rules against, and scores.

The golden rule of this log: record WHAT HAPPENED and the DECISION, never the
sensitive content. We log that an email was headed to an outside domain, not
the customer list in its body; that a query returned 12 rows, not the rows.
A security log is read widely and kept a long time, so it must not become a
second copy of the data you are trying to protect.
"""

import json
import logging
import time
from typing import Any, Dict
from urllib.parse import urlparse

log = logging.getLogger("seclog")

COMPANY_DOMAIN = "bluebird.example.com"
BUILTINS = {"search_docs", "read_file", "fetch_url", "send_email", "query_db", "create_ticket", "run_python"}


def _summary(tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """A safe, content-free description of a tool call."""
    try:
        if tool == "send_email":
            to = str(args.get("to", ""))
            domain = to.split("@")[-1].lower() if "@" in to else ""
            return {"to_domain": domain, "external": bool(domain) and domain != COMPANY_DOMAIN}
        if tool == "fetch_url":
            return {"host": (urlparse(str(args.get("url", ""))).hostname or "").lower()}
        if tool == "read_file":
            path = str(args.get("path", ""))
            return {"escapes_workspace": ".." in path or path.startswith("/")}
        if tool == "query_db":
            sql = str(args.get("sql", "")).lower()
            return {"selects_contact": "email" in sql, "writes": any(w in sql for w in ("insert", "update", "delete", "drop"))}
        if tool == "run_python":
            return {}
        if tool not in BUILTINS:
            return {"builtin": False}
    except Exception:  # a log must never break the agent
        return {}
    return {}


def tool_event(user: str, tool: str, args: Dict[str, Any], decision: str, reason: str = "") -> None:
    event = {
        "event": "tool_call", "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": user, "tool": tool, "builtin": tool in BUILTINS,
        "decision": decision,  # ok | blocked | error
        "summary": _summary(tool, args),
    }
    if reason:
        event["reason"] = reason[:200]
    log.warning(json.dumps(event))


def chat_event(user: str, tools: list, blocked: int, steps: int) -> None:
    log.warning(json.dumps({
        "event": "chat", "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": user, "tool_calls": len(tools), "tools": tools, "blocked": blocked, "steps": steps,
    }))
