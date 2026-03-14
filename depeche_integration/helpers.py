"""Shared helpers for Depeche tool wrappers."""

from __future__ import annotations

import json
import os


async def with_depeche_conn(handler, **handler_kwargs) -> str:
    """Acquire settings + conn, call an async depeche handler, return JSON string."""
    from depeche.config import get_settings
    from depeche.db.connection import get_db, init_db

    settings = get_settings()
    conn = get_db(settings.database_url)
    init_db(conn)
    try:
        result = await handler(conn=conn, settings=settings, **handler_kwargs)
        conn.commit()
        return json.dumps(result)
    finally:
        conn.close()


def check_depeche(*extra_env: str):
    """Return a check_fn that verifies DATABASE_URL + any extra env vars."""
    def _check():
        if not os.getenv("DATABASE_URL"):
            return False
        return all(os.getenv(e) for e in extra_env)
    return _check
