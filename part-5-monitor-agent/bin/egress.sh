#!/usr/bin/env bash
# Demonstrate network egress control: cut the agent off from the "outside"
# network (where the attacker's site lives) and show it can no longer reach it.
#
#   bin/egress.sh test     show whether the agent can reach the attacker site
#   bin/egress.sh on       disconnect the agent from the outside network
#   bin/egress.sh off      reconnect it
#
# A blunt disconnect also blocks the legitimate partner site, because this lab
# puts both on one network. In production you keep the agent on the network but
# route its outbound through an allowlist proxy, so only approved hosts answer.
# The code sandbox shows the ideal in miniature: it has no network at all.
set -euo pipefail
cd "$(dirname "$0")/.."
NET="$(docker compose config --format json 2>/dev/null | python3 -c 'import json,sys;print(json.load(sys.stdin)["name"])')_outside"

reach() {  # does agent-api have a network path to a host?
  docker exec agent-api python -c "
import socket; socket.setdefaulttimeout(3)
try:
    socket.create_connection(('$1', 80)); print('  $1: REACHABLE')
except Exception as e: print('  $1:', type(e).__name__)
" 2>/dev/null || echo "  $1: (agent-api not running)"
}

case "${1:-test}" in
  on)  docker network disconnect "$NET" agent-api 2>/dev/null && echo "Disconnected agent-api from $NET." || echo "Already disconnected."; reach evil.example ;;
  off) docker network connect "$NET" agent-api 2>/dev/null && echo "Reconnected agent-api to $NET." || echo "Already connected."; reach evil.example ;;
  test) echo "Can the agent reach these hosts on the network?"; reach evil.example; reach partner-news.example ;;
  *) echo "usage: bin/egress.sh test|on|off"; exit 1 ;;
esac
