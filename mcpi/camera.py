"""Camera control helpers for the mcpi client.

Provides simple wrappers for camera-related RPCs. Camera setters return
``None`` on success.
"""

from __future__ import annotations

from typing import Optional


class Camera:
    """Camera control wrapper.

    Parameters
    ----------
    mc : mcpi.minecraft.Minecraft
        The parent client used to perform RPC calls.
    """

    def __init__(self, mc) -> None:
        self._mc = mc

    def setNormal(self, entityId: Optional[int] = None) -> None:
        """Set the camera to normal (player) mode or attach to an entity.

        Parameters
        ----------
        entityId : int, optional
            If provided, attach the camera to the given entity id.

        Returns
        -------
        None
        """
        if entityId is None:
            self._mc._request('camera.setNormal')
        else:
            self._mc._request('camera.setNormal', entityId=entityId)
        return None

    def setFixed(self) -> None:
        """Fix the camera to the current position (no following)."""
        self._mc._request('camera.setFixed')
        return None

    def setFollow(self, entityId: int) -> None:
        """Make the camera follow the given entity id."""
        self._mc._request('camera.setFollow', entityId=entityId)
        return None

    def setPos(self, x: float, y: float, z: float) -> None:
        """Set camera position explicitly."""
        self._mc._request('camera.setPos', x=x, y=y, z=z)
        return None
