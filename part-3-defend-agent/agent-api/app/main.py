"""
main.py: the agent's HTTP API (FastAPI).

Routes
  GET  /health   database status and counters
  POST /ingest   add a document to the knowledge base (embedding + insert)
  POST /chat     run the agent for the signed-in user; returns the answer AND
                 the trace of every tool call it made

Who is chatting? NGINX checks each person's API key and passes their name in
the X-Lab-User header. The API also checks the shared edge key it was given,
so nothing that skips NGINX can talk to it.
"""

import hmac
import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from . import db, guards
from .agent import AGENT_MODEL, run_agent
from .embeddings import embed_texts

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("agent-api")

INTERNAL_KEY = open("/run/secrets/internal_api_key", encoding="utf-8").read().strip()
START = time.time()
COUNTS = {"ingested": 0, "chats": 0, "tool_calls": 0, "errors": 0}


class ArticleIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=300)
    url: str = Field(default="", max_length=500)
    source: str = Field(default="", max_length=200)
    text: str = Field(min_length=1, max_length=20000)


class ChatIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=4000)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.open_pools()
    yield
    await db.close_pools()


app = FastAPI(title="Secure AI Agents: HelpBot", lifespan=lifespan)


def caller(request: Request) -> str:
    """Only NGINX knows the internal key, so only NGINX can name the user."""
    if not hmac.compare_digest(request.headers.get("X-Internal-Key", ""), INTERNAL_KEY):
        raise HTTPException(status_code=403, detail="Requests must come through the gateway.")
    user = request.headers.get("X-Lab-User", "")
    if not user:
        raise HTTPException(status_code=401, detail="Unknown user.")
    return user


@app.get("/health")
async def health():
    ok = await db.ready()
    return {"ok": ok, "db_ok": ok, "model": AGENT_MODEL, "defenses": guards.status(), "uptime_s": int(time.time() - START), **COUNTS}


@app.post("/ingest")
async def ingest(article: ArticleIn, user: str = Depends(caller)):
    vec = (await embed_texts([article.text]))[0]
    doc_id = await db.insert_doc(article.model_dump(), vec)
    COUNTS["ingested"] += 1
    return {"status": "ok", "id": doc_id}


@app.post("/chat")
async def chat(payload: ChatIn, user: str = Depends(caller)):
    try:
        result = await run_agent(payload.message, user)
    except Exception as e:
        COUNTS["errors"] += 1
        log.exception("chat failed")
        raise HTTPException(status_code=500, detail=f"Agent error: {type(e).__name__}")
    COUNTS["chats"] += 1
    COUNTS["tool_calls"] += len(result["trace"])
    log.info("chat user=%s steps=%s tools=%s", user, result["steps"], [t["tool"] for t in result["trace"]])
    return {"user": user, **result}
