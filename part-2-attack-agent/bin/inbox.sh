#!/usr/bin/env bash
# List every email the agent has "sent" (they all land in Mailpit, nothing leaves).
# Usage: bin/inbox.sh            list messages
#        bin/inbox.sh clear      delete them all
set -euo pipefail
if [[ "${1:-}" == "clear" ]]; then curl -s -X DELETE http://localhost:8025/api/v1/messages >/dev/null; echo "Inbox cleared."; exit 0; fi
PY_CODE="$(cat <<'PY'
import json, sys
msgs = json.load(sys.stdin).get("messages") or []
print("%d message(s). Full text: http://localhost:8025" % len(msgs))
for m in msgs:
    to = ", ".join(a["Address"] for a in m.get("To") or [])
    print("  to %-38s %-40s  %s" % (to, (m.get("Subject") or "")[:40], (m.get("Snippet") or "")[:60]))
PY
)"
curl -s http://localhost:8025/api/v1/messages | python3 -c "$PY_CODE"
