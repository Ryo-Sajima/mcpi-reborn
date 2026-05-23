"""Player-related convenience helpers for the mcpi client.

This module provides a thin wrapper around the bridge RPC for
player-specific operations. Methods that perform state-changing
operations return ``None`` on success and raise ``MinecraftProtocolError``
on failure (propagated from the underlying connection).
"""

from __future__ import annotations

from typing import Tuple

from .vec3 import Vec3
from .connection import MinecraftProtocolError


class Player:
    """Convenience wrapper for player RPCs.

    Parameters
    ----------
    mc : mcpi.minecraft.Minecraft
        The parent Minecraft client used to perform requests.
    """

    def __init__(self, mc) -> None:
        self._mc = mc

    def getPos(self) -> Vec3[float]:
        """Get the player's precise position.

        Returns
        -------
        Vec3
            ``Vec3`` with floating-point coordinates. Raises
            ``MinecraftProtocolError`` if the bridge returns no result or
            an unexpected payload.
        """
        res = self._mc._request('player.getPos')
        if res is None:
            raise MinecraftProtocolError('player.getPos returned no result')
        # Expect a sequence [x, y, z] or a dict with x/y/z keys.
        if isinstance(res, (list, tuple)) and len(res) >= 3:
            return Vec3(float(res[0]), float(res[1]), float(res[2]))
        if isinstance(res, dict) and all(k in res for k in ("x", "y", "z")):
            return Vec3(float(res["x"]), float(res["y"]), float(res["z"]))
        raise MinecraftProtocolError('unexpected player.getPos response')

    def setPos(self, x: float, y: float, z: float) -> None:
        """Set the player's precise position.

        Parameters
        ----------
        x, y, z : float
            Target coordinates.

        Returns
        -------
        None
        """
        self._mc._request('player.setPos', x=x, y=y, z=z)
        return None

    def getTilePos(self) -> Vec3[int]:
        """Get the player's block-aligned (tile) position.

        Returns
        -------
        Vec3
            ``Vec3`` with integer coordinates (tile positions). Raises
            ``MinecraftProtocolError`` if the bridge returns no result or an
            unexpected payload.
        """
        res = self._mc._request('player.getTilePos')
        if res is None:
            raise MinecraftProtocolError('player.getTilePos returned no result')
        if isinstance(res, (list, tuple)) and len(res) >= 3:
            return Vec3(int(res[0]), int(res[1]), int(res[2]))
        if isinstance(res, dict) and all(k in res for k in ("x", "y", "z")):
            return Vec3(int(res["x"]), int(res["y"]), int(res["z"]))
        raise MinecraftProtocolError('unexpected player.getTilePos response')

    def setTilePos(self, x: int, y: int, z: int) -> None:
        """Set the player's block-aligned (tile) position.

        Parameters
        ----------
        x, y, z : int
            Target tile coordinates.

        Returns
        -------
        None
        """
        self._mc._request('player.setTilePos', x=x, y=y, z=z)
        return None

    def getRotation(self) -> float:
        """Get the player's rotation (yaw) in degrees.

        Returns
        -------
        float
            Rotation angle in degrees. Raises ``MinecraftProtocolError`` if
            unavailable.
        """
        res = self._mc._request('player.getRotation')
        if isinstance(res, (int, float)):
            return float(res)
        raise MinecraftProtocolError('unexpected player.getRotation response')

    def getPitch(self) -> float:
        """Get the player's pitch in degrees.

        Returns
        -------
        float
            Pitch angle in degrees. Raises ``MinecraftProtocolError`` if
            unavailable.
        """
        res = self._mc._request('player.getPitch')
        if isinstance(res, (int, float)):
            return float(res)
        raise MinecraftProtocolError('unexpected player.getPitch response')

    def getDirection(self) -> Tuple[float, float, float]:
        """Get the player's forward direction vector.

        Returns
        -------
        tuple[float, float, float]
            Direction vector. Raises ``MinecraftProtocolError`` if unavailable
            or payload is unexpected.
        """
        res = self._mc._request('player.getDirection')
        if res is None:
            raise MinecraftProtocolError('player.getDirection returned no result')
        if isinstance(res, (list, tuple)) and len(res) >= 3:
            return (float(res[0]), float(res[1]), float(res[2]))
        raise MinecraftProtocolError('unexpected player.getDirection response')
