#!/usr/bin/env python3
"""Show the agent's security log.

  bin/logs.py                     recent tool calls and chats
  bin/logs.py --since 15m
  bin/logs.py --tool send_email
  bin/logs.py --decision blocked
  bin/logs.py --user bob
  bin/logs.py --summary           counts by tool and decision
"""
import argparse, json
from seclog import read_events, hhmmss

ap = argparse.ArgumentParser()
ap.add_argument("--since", default="1h"); ap.add_argument("--tool"); ap.add_argument("--decision")
ap.add_argument("--user"); ap.add_argument("--summary", action="store_true"); ap.add_argument("--limit", type=int, default=40)
a = ap.parse_args()

events = read_events(a.since)
tool_events = [e for e in events if e["event"] == "tool_call"]
if a.tool: tool_events = [e for e in tool_events if e["tool"] == a.tool]
if a.decision: tool_events = [e for e in tool_events if e.get("decision") == a.decision]
if a.user: tool_events = [e for e in tool_events if e.get("user") == a.user]

if a.summary:
    from collections import Counter
    print("Tool calls by tool:    ", dict(Counter(e["tool"] for e in tool_events)))
    print("Tool calls by decision:", dict(Counter(e.get("decision") for e in tool_events)))
    chats = [e for e in events if e["event"] == "chat"]
    print(f"Chats: {len(chats)}, blocked tool calls: {sum(e.get('blocked',0) for e in chats)}")
else:
    shown = tool_events[-a.limit:]
    for e in shown:
        extra = json.dumps(e.get("summary") or {})
        reason = ("  " + e["reason"]) if e.get("reason") else ""
        print(f'{hhmmss(e["ts"])}  {e.get("user",""):<6} {e["tool"]:<14} {e.get("decision",""):<8} {extra}{reason[:60]}')
    print(f"({len(shown)} of {len(tool_events)} tool calls)")
