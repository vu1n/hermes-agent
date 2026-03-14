"""Depeche wire tool — poll wire sources for real-time events."""

from tools.registry import registry

SCHEMA = {
    "name": "depeche_wire",
    "description": (
        "Poll wire sources (Twitter/X, Bluesky, breaking RSS) for real-time "
        "events. Dedupes, analyzes, matches against watches, and classifies "
        "priority. Returns P0 notifications for immediate delivery."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sources": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional filter — source names to poll. "
                    "Options: twitter, bluesky, rss_breaking. "
                    "Default: all configured sources."
                ),
            },
        },
        "required": [],
    },
}


async def _handler(args, **kw):
    from depeche.tools.wire import wire_poll_handler
    from depeche_integration.helpers import with_depeche_conn

    return await with_depeche_conn(
        wire_poll_handler,
        sources=args.get("sources"),
    )


from depeche_integration.helpers import check_depeche

registry.register(
    name="depeche_wire",
    toolset="depeche",
    schema=SCHEMA,
    handler=_handler,
    check_fn=check_depeche(),
    requires_env=["DATABASE_URL"],
    is_async=True,
)
