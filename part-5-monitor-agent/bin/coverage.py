#!/usr/bin/env python3
"""
coverage.py: score the last red-team run. For each attack step, did a rule
MEANT for that step fire while it was running? Judge detection by the log,
not by whether the attack was blocked.

  python3 bin/coverage.py            score the most recent run
  python3 bin/coverage.py --report   write a short findings report
"""

import argparse
import glob
import json
import os
from datetime import datetime, timedelta

import seclog

GRACE = timedelta(seconds=8)  # a log line can trail the action by a moment


def latest_run():
    runs = sorted(glob.glob(str(seclog.ROOT / "redteam" / "runs" / "run-*.json")))
    if not runs:
        raise SystemExit("No red-team runs found. Run python3 bin/redteam.py first.")
    return json.load(open(runs[-1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    run = latest_run()
    started = datetime.fromisoformat(run["started"])
    enabled = seclog.load_rules()
    # only events from this run onward, so earlier practice traffic does not count
    events = [e for e in seclog.read_events("2h") if e["ts"] >= started - timedelta(seconds=2)]
    alerts = seclog.detect(events, enabled)
    enabled_ids = {r["id"] for r in enabled}

    rows, detected = [], 0
    for step in run["steps"]:
        s = datetime.fromisoformat(step["start"])
        e = datetime.fromisoformat(step["end"])
        want = step["expected_rules"]
        hit = [a for a in alerts if a["rule"] in want and s - timedelta(seconds=1) <= a["time"] <= e + GRACE]
        # a rule can only "detect" if it is enabled; note when the expected rule is off
        off = [r for r in want if r not in enabled_ids]
        if hit:
            detected += 1
            mark, note = "DETECTED", ", ".join(sorted({a["rule"] for a in hit}))
        elif off and len(off) == len(want):
            mark, note = "no (rule off)", "expected rule disabled: " + ",".join(off)
        else:
            mark, note = "MISSED", "-"
        rows.append((step["id"], step["name"], mark, note))

    print(f'{"STEP":<5} {"ATTACK":<38} {"RESULT":<14} ALERTS')
    print("-" * 92)
    for sid, name, mark, note in rows:
        print(f"{sid:<5} {name:<38} {mark:<14} {note}")
    print("-" * 92)
    print(f"Detection coverage: {detected} of {len(rows)} attack steps "
          f"({100 * detected // max(1, len(rows))}%)")

    if args.report:
        path = seclog.ROOT / "redteam" / f"report-{started.strftime('%Y%m%d-%H%M%S')}.md"
        lines = [f"# Red-team findings, {run['started'][:19]} UTC", "",
                 f"- Steps: {len(rows)}   Detected: {detected} ({100*detected//max(1,len(rows))}%)",
                 f"- Rules enabled: {', '.join(sorted(enabled_ids))}", "", "| Step | Attack | Result | Alerts |", "|---|---|---|---|"]
        lines += [f"| {sid} | {name} | {mark} | {note} |" for sid, name, mark, note in rows]
        path.write_text("\n".join(lines) + "\n")
        print(f"\nReport written to {path.relative_to(seclog.ROOT)}")


if __name__ == "__main__":
    main()
