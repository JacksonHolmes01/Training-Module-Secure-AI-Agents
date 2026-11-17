"""
gradio-ui/app.py: browser chat UI for the HelpBot agent.

Pick who you are (alice or bob). The UI sends that person's API key to
NGINX, server-side; keys never reach the browser. Each answer shows the
tools the agent called, so you can see what it DID, not just what it said.
"""

import json
import os

import gradio as gr
import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://nginx:8088").rstrip("/")
KEYS = {"alice": os.getenv("ALICE_API_KEY", ""), "bob": os.getenv("BOB_API_KEY", "")}


def chat_fn(message: str, history: list, user: str) -> str:
    try:
        with httpx.Client(timeout=600) as client:
            r = client.post(f"{API_BASE_URL}/chat", json={"message": message},
                            headers={"X-API-Key": KEYS.get(user, "")})
        if r.status_code != 200:
            return f"Error: HTTP {r.status_code}: {r.text[:300]}"
        d = r.json()
    except httpx.TimeoutException:
        return "The agent took too long. The model may still be loading; try again."
    except Exception as e:
        return f"UI could not reach the API: {type(e).__name__}"

    out = d.get("answer", "")
    if d.get("trace"):
        out += "\n\n---\n**What the agent did:**\n"
        for t in d["trace"]:
            mark = "" if t.get("ok") else " (failed)"
            out += f"- `{t['tool']}` `{json.dumps(t['args'])[:150]}`{mark}\n"
    return out


with gr.Blocks(title="Secure AI Agents: HelpBot") as demo:
    gr.Markdown(
        "# HelpBot, the support team's agent\n"
        "HelpBot can search the knowledge base, read workspace files, fetch web pages, "
        "query the customer database, create tickets, and send email.\n\n"
        "Sent email lands in the fake inbox at http://localhost:8025. Nothing leaves your computer."
    )
    user = gr.Radio(["alice", "bob"], value="alice", label="You are",
                    info="alice: support agent.  bob: intern (may not view customer contact details).")
    gr.ChatInterface(chat_fn, type="messages", additional_inputs=[user])

demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False)
