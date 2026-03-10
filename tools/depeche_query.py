"""Depeche query tool — fan-out search across knowledge sources."""

from tools.registry import registry

_DEFAULT_SOURCES = ["artifacts", "graph", "memory", "session", "interests"]

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
                "default": _DEFAULT_SOURCES,
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
    from depeche.tools.query import query_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(
        query_handler,
        q=args["q"],
        sources=args.get("sources", _DEFAULT_SOURCES),
        top_k=args.get("top_k", 10),
    )


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_query",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
