"""Depeche intake tool — run the feed intake loop."""

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
        "required": [],
    },
}


async def _handler(args, **kw):
    from depeche.ingestion.videpoches import run_intake
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(run_intake, feeds=args.get("feeds"))


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_intake",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
