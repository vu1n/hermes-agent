"""Depeche research tool — deep research on a question."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_research",
    "description": (
        "Run deep research on a question. Queries knowledge sources, builds "
        "an evidence pack, and creates a research brief stored in the "
        "database. Returns brief_id for chaining with depeche_publish_brief."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The research question to investigate.",
            },
            "context": {
                "type": "string",
                "default": "",
                "description": "Optional additional context for the research.",
            },
        },
        "required": ["question"],
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.tools.research import research_handler

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await research_handler(
            question=args["question"],
            context=args.get("context", ""),
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL"))


registry.register(
    name="depeche_research",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL"],
    is_async=True,
)
