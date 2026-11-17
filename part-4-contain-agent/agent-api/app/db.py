"""
db.py: database access for the agent.

Two logins, each with its own connection pool:
  kb_ingest  adds documents to the knowledge base (used only by /ingest)
  agent_app  everything the agent does: search documents, read customers,
             create tickets

agent_app is the same login no matter WHICH person is chatting. That is how
many agent tutorials are built, and it is one of the weaknesses Part 2 attacks.
Passwords come from Docker secret files, never from environment variables.
"""

import os
from typing import Any, Dict, List

from . import guards

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

DB_HOST   = os.getenv("DB_HOST", "pgvector")
DB_NAME   = os.getenv("DB_NAME", "agentlab")
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))


def _secret(name: str) -> str:
    with open(f"/run/secrets/{name}", encoding="utf-8") as f:
        return f.read().strip()


def _pool(role: str, max_size: int) -> AsyncConnectionPool:
    conninfo = (f"host={DB_HOST} dbname={DB_NAME} user={role} "
                f"password={_secret(role + '_password')} application_name=agent-api-{role}")
    return AsyncConnectionPool(conninfo, min_size=1, max_size=max_size, open=False,
                               check=AsyncConnectionPool.check_connection)


ingest_pool = _pool("kb_ingest", 2)
agent_pool = _pool("agent_app", 6)


async def open_pools() -> None:
    await ingest_pool.open()
    await agent_pool.open()


async def close_pools() -> None:
    await ingest_pool.close()
    await agent_pool.close()


def vector_literal(vec: List[float]) -> str:
    if len(vec) != EMBED_DIM:
        raise ValueError(f"Embedding has {len(vec)} dimensions, expected {EMBED_DIM}.")
    return "[" + ",".join(f"{float(x):.7g}" for x in vec) + "]"


async def ready() -> bool:
    try:
        async with agent_pool.connection() as conn, conn.cursor() as cur:
            await cur.execute("SELECT 1")
            return True
    except Exception:
        return False


async def insert_doc(doc: Dict[str, Any], embedding: List[float]) -> int:
    async with ingest_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            "INSERT INTO kb.documents (title, url, source, content, embedding) "
            "VALUES (%s, %s, %s, %s, %s::vector) RETURNING id",
            (doc.get("title", ""), doc.get("url", ""), doc.get("source", ""), doc["text"], vector_literal(embedding)),
        )
        return (await cur.fetchone())["id"]


async def search(embedding: List[float], k: int) -> List[Dict[str, Any]]:
    v = vector_literal(embedding)
    async with agent_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            "SELECT id, title, url, content, embedding <=> %s::vector AS distance "
            "FROM kb.documents ORDER BY embedding <=> %s::vector LIMIT %s", (v, v, k))
        return await cur.fetchall()


SENIOR_USERS = {u.strip() for u in os.getenv("SENIOR_USERS", "alice").split(",") if u.strip()}


async def run_sql(sql: str, user: str = "", max_rows: int = 50) -> Dict[str, Any]:
    """Run the model's SQL as agent_app. The login can only SELECT customers and
    SELECT/INSERT tickets, so the database itself refuses anything else.

    With DEFEND_DATA on, the query is scoped to the person chatting: row-level
    security on crm.customers then shows a junior user only their own accounts."""
    async with agent_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        if guards.on("DEFEND_DATA") and user:
            await cur.execute("SELECT set_config('app.enforce','on',true), "
                              "set_config('app.current_user',%s,true), "
                              "set_config('app.is_senior',%s,true)",
                              (user, "true" if user in SENIOR_USERS else "false"))
        await cur.execute(sql)
        if cur.description is None:
            return {"rows": [], "rowcount": cur.rowcount}
        rows = await cur.fetchmany(max_rows)
        return {"rows": [{k: (v if isinstance(v, (int, float, str, type(None))) else str(v)) for k, v in r.items()} for r in rows]}


async def create_ticket(customer_id: int, summary: str, created_by: str) -> int:
    async with agent_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            "INSERT INTO crm.tickets (customer_id, summary, created_by) VALUES (%s, %s, %s) RETURNING id",
            (customer_id, summary, created_by))
        return (await cur.fetchone())["id"]


async def is_customer_email(address: str) -> bool:
    """True if this address belongs to a customer in the database. Used by the
    email guard so the agent can still email customers, just not outsiders."""
    async with agent_pool.connection() as conn, conn.cursor() as cur:
        await cur.execute("SELECT 1 FROM crm.customers WHERE lower(email) = lower(%s) LIMIT 1", (address,))
        return (await cur.fetchone()) is not None
