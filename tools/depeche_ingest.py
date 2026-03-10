"""Depeche ingest tool — extract, process, and store a URL as an artifact."""

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
    from depeche.tools.ingest import ingest_url_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(ingest_url_handler, url=args["url"])


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_ingest",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche("FIRECRAWL_API_KEY"),
    requires_env=["DATABASE_URL", "FIRECRAWL_API_KEY"],
    is_async=True,
)
