#!/usr/bin/env bash
# Ask the agent something as alice or bob, and see every tool call it made.
#
# Usage: bin/ask.sh <alice|bob> "your request"
set -euo pipefail
cd "$(dirname "$0")/.."
WHO="${1:?usage: bin/ask.sh <alice|bob> \"request\"}"; MSG="${2:?usage: bin/ask.sh <alice|bob> \"request\"}"
case "$WHO" in alice|bob) ;; *) echo "user must be alice or bob"; exit 1 ;; esac
VAR="$(echo "$WHO" | tr '[:lower:]' '[:upper:]')_API_KEY"
KEY="$(grep -E "^${VAR}=" .env | cut -d= -f2-)"
BODY="$(python3 -c 'import json,sys; print(json.dumps({"message": sys.argv[1]}))' "$MSG")"
PY_CODE="$(cat <<'PY'
import json, sys
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except ValueError:
    sys.exit("Unexpected reply: " + raw[:300])
if "answer" not in d:
    sys.exit("Error: " + json.dumps(d)[:400])
print("User: %s   (%s model calls, %ss)" % (d["user"], d["steps"], d["seconds"]))
for t in d["trace"]:
    mark = "ok" if t["ok"] else "FAILED"
    print("  tool %s(%s)  [%s]" % (t["tool"], json.dumps(t["args"])[:160], mark))
    print("     -> " + t["result"].replace("\n", " ")[:200])
print("Answer: " + d["answer"])
PY
)"
curl -s -X POST http://localhost:8088/chat -H "X-API-Key: $KEY" -H "Content-Type: application/json" -d "$BODY" \
  | python3 -c "$PY_CODE"
