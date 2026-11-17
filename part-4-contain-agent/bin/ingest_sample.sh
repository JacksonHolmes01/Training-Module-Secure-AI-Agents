#!/usr/bin/env bash
# Adds every document in data/kb_articles.jsonl to the knowledge base.
set -uo pipefail
cd "$(dirname "$0")/.."
KEY="$(grep -E '^ALICE_API_KEY=' .env | cut -d= -f2-)"
RESP="$(mktemp)"; trap 'rm -f "$RESP"' EXIT
ok=0; fail=0; n=0
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  n=$((n+1))
  code=$(curl -s -o "$RESP" -w '%{http_code}' -X POST http://localhost:8088/ingest \
    -H "X-API-Key: $KEY" -H "Content-Type: application/json" -d "$line")
  if [[ "$code" == "200" ]]; then ok=$((ok+1))
  elif [[ "$code" == "000" ]]; then echo "  ✘ could not reach localhost:8088. Is the stack running? (docker compose ps)"; exit 1
  else fail=$((fail+1)); echo "  ✘ document $n failed (HTTP $code): $(cat "$RESP")"; fi
  sleep 0.2
done < data/kb_articles.jsonl
echo "Total: $n  Success: $ok  Failed: $fail"
[[ $fail -eq 0 ]]
