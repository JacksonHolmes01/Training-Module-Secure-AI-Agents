"""
seclog.py: read the agent's security log and apply detection rules.
Standard library only. Used by bin/logs.py, bin/detect.py, bin/coverage.py.

Each log line the agent writes is one event:
  {"event":"tool_call","time":...,"user":...,"tool":...,"decision":"ok|blocked",
   "builtin":bool,"summary":{...},"reason":...}
  {"event":"chat","time":...,"user":...,"tool_calls":N,"tools":[...],"blocked":N,"steps":N}

A rule's "match" can test a top-level field or a field inside "summary" with a
dotted key, e.g. {"tool":"send_email","summary.external":true}.
"""

import json
import pathlib
import re
import subprocess
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVENT = re.compile(r"\{.*\}\s*$")


def _ts(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def read_events(since: str = "1h") -> list:
    raw = subprocess.run(
        ["docker", "compose", "logs", "--no-log-prefix", "--no-color", "--since", since, "agent-api"],
        capture_output=True, text=True, cwd=ROOT).stdout
    events = []
    for line in raw.splitlines():
        m = EVENT.search(line)
        if not m:
            continue
        try:
            ev = json.loads(m.group(0))
        except ValueError:
            continue
        if "event" not in ev or "time" not in ev:
            continue
        try:
            ev["ts"] = _ts(ev["time"])
        except ValueError:
            continue
        events.append(ev)
    events.sort(key=lambda e: e["ts"])
    return events


def _get(ev: dict, key: str):
    if "." in key:
        head, rest = key.split(".", 1)
        return (ev.get(head) or {}).get(rest)
    return ev.get(key)


def _matches(ev: dict, match: dict) -> bool:
    for key, want in match.items():
        have = _get(ev, key)
        if isinstance(want, list):
            if have not in want:
                return False
        elif have != want:
            return False
    return True


def load_rules(include_disabled: bool = False) -> list:
    rules = json.loads((ROOT / "detections" / "rules.json").read_text())
    return [r for r in rules if include_disabled or r.get("enabled", True)]


def detect(events: list, rules: list) -> list:
    """Sliding-window threshold detection. An alert fires when `threshold`
    matching events from the same group arrive within `window_s` seconds.
    After firing, the rule stays quiet for that group for one window, so one
    attack produces one alert, not hundreds."""
    alerts = []
    for rule in rules:
        window = timedelta(seconds=rule["window_s"])
        recent = defaultdict(deque)
        quiet_until = {}
        mf = rule.get("min_field")
        for ev in events:
            if not _matches(ev, rule["match"]):
                continue
            if mf and (ev.get(mf[0]) or 0) < mf[1]:   # optional per-event numeric threshold
                continue
            group = str(ev.get(rule.get("group_by", "user"), "") or "-")
            q = recent[group]
            q.append(ev)
            while q and ev["ts"] - q[0]["ts"] > window:
                q.popleft()
            if len(q) >= rule["threshold"] and ev["ts"] >= quiet_until.get(group, ev["ts"]):
                alerts.append({"time": ev["ts"], "rule": rule["id"], "name": rule["name"],
                               "severity": rule["severity"], "group": group, "count": len(q),
                               "first": q[0]["ts"], "why": rule["why"], "response": rule["response"]})
                quiet_until[group] = ev["ts"] + window
                q.clear()
    alerts.sort(key=lambda a: a["time"])
    return alerts


def hhmmss(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%H:%M:%S")
