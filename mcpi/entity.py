"""Entity convenience wrapper for the mcpi client.

Provides simple typed accessors for common entity operations. Setter
methods return ``None`` on success; getter methods return typed
results or ``None`` when the bridge supplies no result.
"""

from __future__ import annotations

from typing import Optional, Tuple


class Entity:
    """Wrapper for entity-related RPCs.

    Parameters
    ----------
    mc : mcpi.minecraft.Minecraft
        The parent client used to perform RPC calls.
    """

    def __init__(self, mc) -> None:
        self._mc = mc

    def getPos(self, entityId: int) -> Optional[Tuple[float, float, float]]:
        """Get an entity's precise position.

        Parameters
        ----------
        entityId : int
            The entity id.

        Returns
        -------
        tuple[float, float, float] | None
            Entity position or ``None``.
        """
        res = self._mc._request('entity.getPos', entityId=entityId)
        if res is None:
            return None
        return tuple(res)

    def setPos(self, entityId: int, x: float, y: float, z: float) -> None:
        """Set an entity's precise position.

        Returns
        -------
        None
        """
        self._mc._request('entity.setPos', entityId=entityId, x=x, y=y, z=z)
        return None

    def getTilePos(self, entityId: int) -> Optional[Tuple[int, int, int]]:
        """Get an entity's block-aligned tile position.

        Returns
        -------
        tuple[int, int, int] | None
        """
        res = self._mc._request('entity.getTilePos', entityId=entityId)
        if res is None:
            return None
        return tuple(res)

    def setTilePos(self, entityId: int, x: int, y: int, z: int) -> None:
        """Set an entity's tile position.

        Returns
        -------
        None
        """
        self._mc._request('entity.setTilePos', entityId=entityId, x=x, y=y, z=z)
        return None

    def getRotation(self, entityId: int) -> Optional[float]:
        """Get an entity's rotation (yaw) in degrees."""
        return self._mc._request('entity.getRotation', entityId=entityId)

    def getPitch(self, entityId: int) -> Optional[float]:
        """Get an entity's pitch in degrees."""
        return self._mc._request('entity.getPitch', entityId=entityId)

    def getDirection(self, entityId: int) -> Optional[Tuple[float, float, float]]:
        """Get the forward direction vector for the entity."""
        res = self._mc._request('entity.getDirection', entityId=entityId)
        if res is None:
            return None
        return tuple(res)
