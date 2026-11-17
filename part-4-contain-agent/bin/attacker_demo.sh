#!/usr/bin/env bash
# Pretend an attacker got code running inside the agent container (through a
# vulnerable library, say). `docker exec` runs each command as the container's
# user, exactly as that attacker would. Run it before and after hardening.
#
# Usage: bin/attacker_demo.sh
set -uo pipefail
C=agent-api

try() {  # try <description> <command>
  if out=$(docker exec "$C" sh -c "$2" 2>&1); then
    printf "  %-46s YES  %s\n" "$1" "$(echo "$out" | head -1 | cut -c1-34)"
  else
    printf "  %-46s no   %s\n" "$1" "$(echo "$out" | tail -1 | cut -c1-34)"
  fi
}

echo "Attacker running inside $C. Can they..."
try "run as root?"                           'test "$(id -u)" = 0 && echo "uid 0 (root)" || { echo "uid $(id -u)"; false; }'
try "read the database password?"            'cat /run/secrets/agent_app_password >/dev/null && echo "read it"'
try "modify the agent's own code?"           'echo "# x" >> /app/app/main.py && echo "patched main.py"'
try "drop a tool in /tmp and run it?"        'printf "#!/bin/sh\necho run\n" > /tmp/x && chmod +x /tmp/x && /tmp/x'
try "install software (apt-get)?"            'apt-get update -qq >/dev/null 2>&1 && echo "apt works"'
try "reach the attacker site on the net?"    'python -c "import socket; socket.setdefaulttimeout(3); socket.create_connection((\"evil.example\",80)); print(\"reached evil.example\")"'
echo
echo "The database password lives in a Docker secret file mounted into this"
echo "container. Hardening cannot hide it from a process that runs AS the agent;"
echo "that is what the sandbox (for the code tool) and network limits are for."
