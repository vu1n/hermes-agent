"""Depeche dossier tool — generate today's daily intelligence dossier."""

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
        "required": [],
    },
}


async def _handler(args, **kw):
    from depeche.tools.dossier import generate_dossier_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(generate_dossier_handler)


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_dossier",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
