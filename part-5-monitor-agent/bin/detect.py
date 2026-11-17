#!/usr/bin/env python3
"""Apply the detection rules to the agent's security log.

  bin/detect.py                 alerts from the last hour
  bin/detect.py --since 15m
  bin/detect.py --rules         list the rules and whether each is enabled
  bin/detect.py --enable A7     turn a rule on   (edits detections/rules.json)
  bin/detect.py --disable A7    turn a rule off
"""
import argparse, json, pathlib
import seclog

ap = argparse.ArgumentParser()
ap.add_argument("--since", default="1h"); ap.add_argument("--rules", action="store_true")
ap.add_argument("--enable"); ap.add_argument("--disable")
a = ap.parse_args()

RULES = pathlib.Path(seclog.ROOT) / "detections" / "rules.json"
if a.enable or a.disable:
    rid, val = (a.enable, True) if a.enable else (a.disable, False)
    data = json.loads(RULES.read_text())
    for r in data:
        if r["id"] == rid: r["enabled"] = val
    RULES.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{'enabled' if val else 'disabled'} {rid}")
elif a.rules:
    for r in json.loads(RULES.read_text()):
        print(f'  {r["id"]}  {"on " if r.get("enabled", True) else "off"}  {r["severity"]:<8} {r["name"]}')
else:
    alerts = seclog.detect(seclog.read_events(a.since), seclog.load_rules())
    if not alerts:
        print("No alerts."); raise SystemExit
    for al in alerts:
        print(f'{seclog.hhmmss(al["time"])}  {al["severity"].upper():<8} {al["rule"]}  {al["name"]}  (user={al["group"]}, x{al["count"]})')
        print(f'     why: {al["why"]}')
