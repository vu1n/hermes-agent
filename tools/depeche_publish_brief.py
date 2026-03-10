"""Depeche publish-brief tool — render and upload a research brief to S3."""

import json
import os

from tools.registry import registry

SCHEMA = {
    "name": "depeche_publish_brief",
    "description": (
        "Publish a research brief to S3. Renders HTML, uploads to storage, "
        "updates the index page. Use after depeche_research to make briefs "
        "accessible via URL. Note: S3_BUCKET should be set for uploads to "
        "succeed."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "brief_id": {
                "type": "string",
                "description": "ID of the research brief to publish.",
            },
        },
        "required": ["brief_id"],
    },
}


async def _handler(args, **kw):
    from depeche.config import get_settings
    from depeche.db.connection import get_db
    from depeche.tools.publish import publish_brief_handler

    settings = get_settings()
    conn = get_db(settings.database_url)
    try:
        result = await publish_brief_handler(
            brief_id=args["brief_id"],
            conn=conn,
            settings=settings,
        )
        return json.dumps(result)
    finally:
        conn.close()


def _check():
    return bool(os.getenv("DATABASE_URL"))


registry.register(
    name="depeche_publish_brief",
    toolset="depeche",
    schema=SCHEMA,
    handler=lambda args, **kw: _handler(args, **kw),
    check_fn=_check,
    requires_env=["DATABASE_URL"],
    is_async=True,
)
