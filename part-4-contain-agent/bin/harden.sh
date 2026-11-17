#!/usr/bin/env bash
# Turn the container hardening overlay on or off, then rebuild and restart.
# Compose reads COMPOSE_FILE from .env, so after this every `docker compose`
# command uses the same set of files.
#
# Usage: bin/harden.sh on | off | status
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="docker-compose.yml"
HARD="docker-compose.yml:hardening/harden.yml"

case "${1:-}" in
  status) grep -E '^COMPOSE_FILE=' .env 2>/dev/null || echo "COMPOSE_FILE=$BASE (default)"; exit 0 ;;
  on)  CF="$HARD" ;;
  off) CF="$BASE" ;;
  *) echo "usage: bin/harden.sh on|off|status"; exit 1 ;;
esac
if grep -qE '^COMPOSE_FILE=' .env; then sed -i.bak "s|^COMPOSE_FILE=.*|COMPOSE_FILE=${CF}|" .env && rm -f .env.bak
else echo "COMPOSE_FILE=${CF}" >> .env; fi
echo "COMPOSE_FILE=${CF}"
echo "Rebuilding and restarting (this recreates changed containers)..."
docker compose up -d --build --remove-orphans >/dev/null 2>&1 || docker compose up -d --build --remove-orphans
KEY="$(grep -E '^ALICE_API_KEY=' .env | cut -d= -f2-)"
for i in $(seq 1 60); do
  curl -s -H "X-API-Key: $KEY" http://localhost:8088/health 2>/dev/null | grep -q '"ok":true' && { echo "Stack is up."; exit 0; }
  sleep 3
done
echo "Did not come up. Check: docker compose ps -a && docker compose logs agent-api --tail=30"; exit 1
