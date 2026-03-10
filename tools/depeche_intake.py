"""Depeche intake tool — run the feed intake loop."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_intake",
    "description": (
        "Run the feed intake loop. Fetches new articles from configured "
        "RSS/HN feeds and ingests them."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "feeds": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
                "description": (
                    "Optional list of feed definitions (name, type, url). "
                    "Uses configured defaults when omitted."
                ),
            },
        },
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.ingestion.videpoches import run_intake

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await run_intake(
            feeds=args.get("feeds"),
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL"))


registry.register(
    name="depeche_intake",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL"],
    is_async=True,
)
