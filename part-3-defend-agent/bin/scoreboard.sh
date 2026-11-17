#!/usr/bin/env bash
# Turn on the defenses one at a time and re-run the attacks after each, so you
# can watch the attacks that succeed drop toward zero.
#
# Usage: bin/scoreboard.sh [tries]   (tries per attack, default 2)
set -euo pipefail
cd "$(dirname "$0")/.."
TRIES="${1:-2}"
LEVELS=("0 none (Part 2 baseline)" "1 + confine file paths" "2 + email allowlist" \
        "3 + fetch allowlist" "4 + approved tools only" "5 + per-user data")
for entry in "${LEVELS[@]}"; do
  n="${entry%% *}"; label="${entry#* }"
  bin/defend.sh level "$n" >/dev/null
  echo "================================================================"
  echo "Level $label"
  echo "================================================================"
  python3 attacks/run_attacks.py --tries "$TRIES" | grep -E 'SUCCEEDED|no effect|see answer|data-theft'
  echo
done
