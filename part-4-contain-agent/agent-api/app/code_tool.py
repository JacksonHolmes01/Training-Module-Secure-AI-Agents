"""
code_tool.py: the run_python tool, and the two ways it can run code.

run_python lets the agent run a short Python snippet to compute something: a
date calculation, a quick total, parsing a number out of text. Real agents
offer this, and it is the single most dangerous capability an agent can have,
because "run code" is "do anything the code's container can do."

  SANDBOX_CODE off  -> run it right here, inside the agent's own container.
                       That container has the network, the mounted workspace,
                       and the agent's database secrets. Malicious code gets
                       all of it. This is the dangerous baseline.

  SANDBOX_CODE on   -> hand the code to the sandbox container through a shared
                       folder and wait for the result. The sandbox has no
                       network, a read-only filesystem, no secrets, and tight
                       limits, so the same code can compute but cannot harm.
"""

import asyncio
import os
import pathlib
import subprocess
import uuid

from . import guards

SANDBOX_DIR = pathlib.Path(os.getenv("SANDBOX_DIR", "/sandbox"))
TIMEOUT_S = float(os.getenv("CODE_TIMEOUT_S", "8"))


async def _run_in_process(code: str) -> str:
    """Dangerous: runs in the agent container, with its network and secrets."""
    proc = await asyncio.create_subprocess_exec(
        "python", "-I", "-c", code,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
    )
    try:
        out, _ = await asyncio.wait_for(proc.communicate(), TIMEOUT_S)
    except asyncio.TimeoutError:
        proc.kill()
        return "code did not finish in time"
    return (out.decode("utf-8", "replace").strip() or "(no output)")[:4000]


async def _run_in_sandbox(code: str) -> str:
    """Contained: hand the code to the no-network sandbox container."""
    job_id = uuid.uuid4().hex
    inbox = SANDBOX_DIR / "in"
    outbox = SANDBOX_DIR / "out"
    inbox.mkdir(parents=True, exist_ok=True)
    outbox.mkdir(parents=True, exist_ok=True)
    result = outbox / f"{job_id}.out"
    (inbox / f"{job_id}.py").write_text(code, encoding="utf-8")
    deadline = asyncio.get_event_loop().time() + TIMEOUT_S + 4
    while asyncio.get_event_loop().time() < deadline:
        if result.exists():
            text = result.read_text(encoding="utf-8", errors="replace")
            try:
                result.unlink()
            except FileNotFoundError:
                pass
            return text[:4000]
        await asyncio.sleep(0.2)
    return "sandbox did not return a result in time (is the sandbox container running?)"


async def run_python(args, user: str) -> str:
    code = str(args.get("code", ""))
    if guards.on("SANDBOX_CODE"):
        return await _run_in_sandbox(code)
    return await _run_in_process(code)
