"""Depeche notify tool — dispatch wire notifications."""

from tools.registry import registry

SCHEMA = {
    "name": "depeche_notify",
    "description": (
        "Dispatch wire notifications. Use action=digest to build a P1 digest "
        "of recent wire events. Use action=status to check the notification "
        "queue."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action: digest (build P1 digest), status (queue status).",
                "default": "digest",
            },
        },
        "required": [],
    },
}


async def _handler(args, **kw):
    from depeche.tools.notify import notify_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(
        notify_handler,
        action=args.get("action", "digest"),
    )


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_notify",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
