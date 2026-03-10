"""Depeche context injection for Hermes system prompt."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def depeche_prefetch() -> str:
    """Called once on first turn to inject Depeche context into system prompt.

    Returns a markdown block with active interests, hot clusters,
    key entities, and knowledge stats. Returns empty string if
    depeche is not installed or no data is available.
    """
    try:
        from depeche.config import get_settings
        from depeche.context.builder import build_context_block
        from depeche.db.connection import get_db
    except ImportError:
        logger.debug("depeche not installed, skipping context injection")
        return ""

    try:
        settings = get_settings()
        conn = get_db(settings.database_url)
        try:
            return build_context_block(conn, settings)
        finally:
            conn.close()
    except Exception:
        logger.debug("depeche context prefetch failed", exc_info=True)
        return ""
