"""Depeche query tool — fan-out search across knowledge sources."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_query",
    "description": (
        "Search across Depeche knowledge sources (artifacts, graph, memory, "
        "session, interests). Fan-out to requested backends, merge and "
        "deduplicate results."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "q": {
                "type": "string",
                "description": "Natural-language search query.",
            },
            "sources": {
                "type": "array",
                "items": {"type": "string"},
                "default": [
                    "artifacts",
                    "graph",
                    "memory",
                    "session",
                    "interests",
                ],
                "description": (
                    "Knowledge sources to query. Defaults to all five: "
                    "artifacts, graph, memory, session, interests."
                ),
            },
            "top_k": {
                "type": "integer",
                "default": 10,
                "description": "Maximum number of results to return.",
            },
        },
        "required": ["q"],
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.tools.query import query_handler

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await query_handler(
            q=args["q"],
            sources=args.get(
                "sources",
                ["artifacts", "graph", "memory", "session", "interests"],
            ),
            top_k=args.get("top_k", 10),
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL"))


registry.register(
    name="depeche_query",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL"],
    is_async=True,
)
