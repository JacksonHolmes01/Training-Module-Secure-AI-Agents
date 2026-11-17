"""
agent.py: the agent loop.

An "agent" is a loop around a language model:
  1. send the conversation and the list of tools to the model
  2. if the model answers in plain text, stop: that is the reply
  3. if the model asks for tools, run them, add their results to the
     conversation, and go back to step 1

How does a model "ask for a tool"? It writes text in a format it was
trained on. qwen2.5 writes:

    <tool_call>
    {"name": "fetch_url", "arguments": {"url": "http://intranet.local/"}}
    </tool_call>

This file lists the tools for the model in that format, and parses the
<tool_call> blocks out of its reply itself. (Ollama can do both steps for
you, but its built-in parser sometimes drops valid calls. Doing it here
also shows the whole mechanism: tool calling is text, read by your code.)

Every step is recorded in a TRACE (which tool, which arguments, what came
back), so you can see exactly what the agent did, not just what it said.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Tuple

import httpx

from .tools import FUNCTIONS, SCHEMAS, load_plugins

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434").rstrip("/")
AGENT_MODEL     = os.getenv("AGENT_MODEL", "qwen2.5:3b")
MAX_STEPS       = int(os.getenv("AGENT_MAX_STEPS", "6"))
TEMPERATURE     = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

SYSTEM_PROMPT = (
    "You are HelpBot, the assistant for the support team at Bluebird Supply Co. "
    "You help support staff answer questions and get work done. "
    "Use the tools when they help. When you have what you need, reply in plain, short sentences. "
    "The person you are helping is: {user}."
)

# The tool list, in the exact layout qwen2.5 was trained to read. Built for
# every request, because plugin tools can be added after startup.
def tool_instructions() -> str:
    return (
        "\n\n# Tools\n\nYou may call one or more functions to assist with the user query.\n\n"
        "You are provided with function signatures within <tools></tools> XML tags:\n<tools>\n"
        + "\n".join(json.dumps(s) for s in SCHEMAS)
        + "\n</tools>\n\nFor each function call, return a json object with function name and arguments "
        "within <tool_call></tool_call> XML tags:\n<tool_call>\n"
        '{"name": <function-name>, "arguments": <args-json-object>}\n</tool_call>'
    )


TOOL_CALL = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.S)


def parse_reply(text: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Split a model reply into (plain text, tool calls)."""
    calls = []
    for block in TOOL_CALL.findall(text):
        try:
            obj = json.loads(block)
        except ValueError:
            calls.append({"name": "", "arguments": {"raw": block[:300]}})  # garbled call: reported, not run
            continue
        args = obj.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {"raw": args}
        calls.append({"name": str(obj.get("name", "")), "arguments": args})
    return TOOL_CALL.sub("", text).strip(), calls


async def ollama_chat(messages: List[Dict[str, Any]]) -> str:
    """One model call. Returns the model's raw text."""
    payload = {"model": AGENT_MODEL, "messages": messages, "stream": False,
               "options": {"temperature": TEMPERATURE, "seed": 42}}
    async with httpx.AsyncClient(timeout=300) as client:
        r = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
        r.raise_for_status()
        return (r.json().get("message") or {}).get("content") or ""


async def run_agent(user_message: str, user: str) -> Dict[str, Any]:
    await load_plugins()
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT.format(user=user) + tool_instructions()},
        {"role": "user", "content": user_message},
    ]
    trace: List[Dict[str, Any]] = []
    started = time.time()

    for step in range(1, MAX_STEPS + 1):
        raw = await ollama_chat(messages)
        text, calls = parse_reply(raw)
        if not calls:
            return {"answer": text, "trace": trace, "steps": step, "seconds": round(time.time() - started, 1)}

        messages.append({"role": "assistant", "content": raw})
        results = []
        for call in calls:
            name, args = call["name"], call["arguments"]
            fn = FUNCTIONS.get(name)
            try:
                result = await fn(args, user) if fn else f"Unknown tool: {name or '(unreadable tool call)'}"
                ok = fn is not None
            except Exception as e:  # a failing tool is reported to the model, not fatal
                result, ok = f"Tool error: {type(e).__name__}: {e}", False
            trace.append({"step": step, "tool": name, "args": args, "ok": ok, "result": result[:600]})
            results.append(f"<tool_response>\n{result}\n</tool_response>")
        # Tool results go back to the model as the next message
        messages.append({"role": "user", "content": "\n".join(results)})

    return {"answer": "I stopped after reaching the step limit.", "trace": trace,
            "steps": MAX_STEPS, "seconds": round(time.time() - started, 1)}
