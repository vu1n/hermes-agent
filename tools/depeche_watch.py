"""Depeche watch tool — manage wire watches for push notifications."""

from tools.registry import registry

SCHEMA = {
    "name": "depeche_watch",
    "description": (
        "Manage wire watches that drive push notifications. Watches match "
        "incoming wire events to trigger P0 (immediate), P1 (digest), or "
        "P2 (dossier) notifications. Actions: create, list, get, update, "
        "delete, enable, disable."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": (
                    "Action to perform: create, list, get, update, delete, "
                    "enable, disable."
                ),
                "default": "list",
            },
            "name": {
                "type": "string",
                "description": "Human name for the watch (required for create).",
            },
            "watch_type": {
                "type": "string",
                "description": (
                    "Watch type: topic, entity, story, keyword. "
                    "Default: topic."
                ),
                "default": "topic",
            },
            "query": {
                "type": "string",
                "description": "Search query or keyword for the watch.",
            },
            "priority": {
                "type": "string",
                "description": (
                    "Notification tier: P0 (immediate, requires verification), "
                    "P1 (2-hourly digest), P2 (daily dossier). Default: P1."
                ),
                "default": "P1",
            },
            "watch_id": {
                "type": "string",
                "description": "Watch ID (required for get/update/delete/enable/disable).",
            },
        },
        "required": [],
    },
}


async def _handler(args, **kw):
    from depeche.tools.watch import watch_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(
        watch_handler,
        action=args.get("action", "list"),
        name=args.get("name", ""),
        watch_type=args.get("watch_type", "topic"),
        query=args.get("query", ""),
        priority=args.get("priority", "P1"),
        watch_id=args.get("watch_id", ""),
    )


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_watch",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
