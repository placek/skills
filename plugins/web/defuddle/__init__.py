"""Defuddle extract backend — user plugin, registered as the ``defuddle`` web provider."""
from __future__ import annotations

from .provider import DefuddleExtractProvider


def register(ctx) -> None:
    ctx.register_web_search_provider(DefuddleExtractProvider())
