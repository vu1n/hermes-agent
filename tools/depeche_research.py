"""Depeche research tool — deep research on a question."""

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
    from depeche.tools.research import research_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(
        research_handler,
        question=args["question"],
        context=args.get("context", ""),
    )


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_research",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
