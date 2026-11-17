# Lesson 4: The Sandbox

Code the agent runs should run somewhere that can compute an answer and do nothing else: no network, no secrets, no lasting disk, strict limits. That is a sandbox.

## What the sandbox is

Open `docker-compose.yml` and find the `sandbox` service:

```yaml
  sandbox:
    build: { context: ./sandbox }
    user: "10001:10001"          # not root
    network_mode: none           # NO network at all
    read_only: true              # its own filesystem cannot be changed
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    mem_limit: 256m
    pids_limit: 64               # a fork bomb hits a wall
    tmpfs:
      - /tmp:noexec,nosuid,size=32m
      - /work:...size=32m
    volumes:
      - sandbox_queue:/sandbox   # the only way in or out: a shared folder
```

The agent and the sandbox share one folder. The agent drops a snippet in; the sandbox (`sandbox/runner.py`) runs it with a five-second timeout and writes back what it printed. The sandbox holds none of the agent's secrets and has no network, so even hostile code is stuck.

## Turn it on

```bash
bin/defend.sh sandbox on
```

Now run the **exact same malicious snippet** from Lesson 3, through the sandbox:

```bash
docker exec agent-api python -c "
import asyncio
from app import code_tool
code = '''
import glob
print('secrets I can see:', glob.glob('/run/secrets/*'))
import socket; socket.setdefaulttimeout(3)
try:
    socket.create_connection(('evil.example', 80)); print('network: reached evil.example')
except Exception as e: print('network:', type(e).__name__)
'''
print(asyncio.run(code_tool._run_in_sandbox(code)))
"
```

```
secrets I can see: []
network: gaierror
```

No secrets exist in the sandbox, and the network is gone (`gaierror` means the name cannot even be looked up). The attacker's code ran, and got nothing. And the agent's real work is unaffected:

```bash
bin/ask.sh alice "Use python to add up the numbers 1 through 10."
```

```
Answer: 55.
```

## Why this is the right shape

The sandbox does not try to decide whether a snippet is safe. It assumes every snippet is hostile and removes everything a hostile snippet would want. That is far more robust than inspecting code, because you cannot reliably tell safe code from clever malicious code, just as you cannot reliably tell a user's instructions from an injected one.

> **The pattern.** Give the riskiest capability the least power. Code execution needs the CPU and nothing else, so give it the CPU and nothing else.

Next: [Least Privilege for Every Container](05-least-privilege.md)
