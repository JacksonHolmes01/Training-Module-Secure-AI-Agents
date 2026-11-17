#!/usr/bin/env bash
# Show every request that reached the OUTSIDE website (partner-news.example / evil.example).
set -euo pipefail
cd "$(dirname "$0")/.."
PY_CODE="$(cat <<'PY'
import json, sys
n = 0
for line in sys.stdin:
    try:
        e = json.loads(line)
    except ValueError:
        continue
    n += 1
    extra = ("  body=" + e["body"][:80]) if e.get("body") else ""
    print("  %s  %-4s %-22s %s%s" % (e["time"][11:19], e["method"], e["host"], e["path"][:120], extra))
print("%d request(s) reached the outside site." % n)
PY
)"
docker compose logs --no-log-prefix external-site 2>/dev/null | python3 -c "$PY_CODE"
