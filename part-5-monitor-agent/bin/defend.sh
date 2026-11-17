#!/usr/bin/env bash
# Turn the agent's defenses on or off, then restart the agent so they take effect.
#
# Usage:
#   bin/defend.sh status                 show which defenses are on
#   bin/defend.sh <name> <on|off>        set one defense
#   bin/defend.sh all <on|off>           set every defense
#   bin/defend.sh level <0-6>            turn on the first N defenses (the lesson order)
#
# Names: paths email url tools data approval spotlight
set -euo pipefail
cd "$(dirname "$0")/.."

ORDER=(PATHS EMAIL URL TOOLS DATA APPROVAL SPOTLIGHT)

show() { grep -E '^DEFEND_' .env | sed 's/^/  /'; }
set_one() {  # set_one <VAR> <true|false>
  if grep -qE "^$1=" .env; then sed -i.bak "s/^$1=.*/$1=$2/" .env && rm -f .env.bak
  else echo "$1=$2" >> .env; fi
}
restart() {
  echo "Restarting the agent with:"; grep -E '^DEFEND_' .env | grep '=true' | sed 's/^/  /' || echo "  (no defenses on)"
  docker compose up -d agent-api >/dev/null 2>&1
  for i in $(seq 1 40); do
    docker inspect -f '{{.State.Health.Status}}' agent-api 2>/dev/null | grep -q healthy && { echo "Agent ready."; return 0; }
    sleep 2
  done
  echo "Agent did not become healthy. Check: docker compose logs agent-api --tail=30"; exit 1
}

case "${1:-}" in
  status) show; exit 0 ;;
  level)
    n="${2:?usage: bin/defend.sh level <0-6>}"
    for i in "${!ORDER[@]}"; do
      [[ $i -lt $n ]] && set_one "DEFEND_${ORDER[$i]}" true || set_one "DEFEND_${ORDER[$i]}" false
    done
    restart ;;
  all)
    v=$([[ "${2:-}" == "on" ]] && echo true || echo false)
    for d in "${ORDER[@]}"; do set_one "DEFEND_$d" "$v"; done
    restart ;;
  sandbox)
    v=$([[ "${2:-}" == "on" ]] && echo true || echo false)
    set_one SANDBOX_CODE "$v"; restart ;;
  paths|email|url|tools|data|approval|spotlight)
    v=$([[ "${2:-}" == "on" ]] && echo true || echo false)
    set_one "DEFEND_$(echo "$1" | tr '[:lower:]' '[:upper:]')" "$v"
    restart ;;
  *) echo "usage: bin/defend.sh <status|level N|all on|off|<name> on|off>"; exit 1 ;;
esac
