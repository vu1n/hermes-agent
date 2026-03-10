"""Depeche ingest tool — extract, process, and store a URL as an artifact."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_ingest",
    "description": (
        "Extract, process, and store a URL as an article artifact. Runs "
        "extraction, chunking, embedding, clustering, and graph edge creation."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL to extract and ingest.",
            },
        },
        "required": ["url"],
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.tools.ingest import ingest_url_handler

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await ingest_url_handler(
            url=args["url"],
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL")) and bool(os.getenv("FIRECRAWL_API_KEY"))


registry.register(
    name="depeche_ingest",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL", "FIRECRAWL_API_KEY"],
    is_async=True,
)
