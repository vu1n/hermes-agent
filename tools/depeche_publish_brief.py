"""Depeche publish-brief tool — render and upload a research brief to S3."""

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
    from depeche.tools.publish import publish_brief_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(publish_brief_handler, brief_id=args["brief_id"])


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_publish_brief",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
