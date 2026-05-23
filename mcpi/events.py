"""Event helpers for the mcpi client.

This module provides simple wrappers to poll or clear event queues
exposed by the server bridge.
"""

from __future__ import annotations

from typing import Optional, List, Dict


class Events:
    """Wrapper around event-related RPCs."""

    def __init__(self, mc) -> None:
        self._mc = mc

    def pollBlockHits(self) -> None:
        """Poll block-hit events.

        Not implemented in the Python client layer; the bridge may support
        similar functionality in the future.
        """
        raise NotImplementedError("events.pollBlockHits is not implemented on the Python client")

    def pollChatPosts(self) -> Optional[List[Dict[str, object]]]:
        """Return a list of recent chat events, or ``None``.

        Returns
        -------
        list[dict] | None
            Chat event dicts or ``None`` if no result.
        """
        return self._mc._request('events.pollChatPosts')

    def clearAll(self) -> None:
        """Clear all pending events."""
        self._mc._request('events.clearAll')
        return None
