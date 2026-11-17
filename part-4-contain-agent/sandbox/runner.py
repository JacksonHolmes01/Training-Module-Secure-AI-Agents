"""
runner.py: the code sandbox.

This process runs inside a container that has NO network, a read-only root
filesystem, a non-root user, and tight memory and process limits. It watches
a shared folder for Python snippets the agent wants to run, executes each one
with a short timeout, and writes back whatever it printed.

Because this container cannot reach the network, cannot write outside its
scratch space, and holds none of the agent's secrets, code that runs here can
compute an answer but can do nothing else. A malicious snippet is contained.
"""

import pathlib
import subprocess
import time

Q = pathlib.Path("/sandbox")
IN = Q / "in"
OUT = Q / "out"
for d in (IN, OUT):
    d.mkdir(parents=True, exist_ok=True)

print("sandbox runner started", flush=True)
while True:
    for job in sorted(IN.glob("*.py")):
        code = job.read_text(encoding="utf-8", errors="replace")
        try:
            job.unlink()
        except FileNotFoundError:
            continue
        try:
            # -I: isolated mode (ignore env and the current dir for imports)
            r = subprocess.run(["python", "-I", "-c", code], capture_output=True,
                               text=True, timeout=5, cwd="/work")
            out = (r.stdout + r.stderr).strip() or "(no output)"
        except subprocess.TimeoutExpired:
            out = "sandbox: code did not finish within 5 seconds and was stopped"
        except Exception as e:  # noqa: BLE001 - report anything back to the agent
            out = f"sandbox error: {type(e).__name__}: {e}"
        (OUT / (job.stem + ".out")).write_text(out[:4000], encoding="utf-8")
    time.sleep(0.2)
