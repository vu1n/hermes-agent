"""Depeche dossier tool — generate today's daily intelligence dossier."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_dossier",
    "description": (
        "Generate today's daily intelligence dossier. Ranks recent articles "
        "by interest fit and novelty, renders HTML, and publishes to S3."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.tools.dossier import generate_dossier_handler

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await generate_dossier_handler(
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL"))


registry.register(
    name="depeche_dossier",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL"],
    is_async=True,
)
