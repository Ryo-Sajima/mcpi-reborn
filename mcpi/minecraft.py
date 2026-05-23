"""mcpi client library.

This module exposes :class:`Minecraft`, a thin client that communicates
with the Fabric TCP/JSON bridge. The API mirrors the mcpi conventions but
adds stronger typing and clearer error handling.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from .connection import Connection, MinecraftConnectionError, MinecraftProtocolError
from .player import Player
from .block import Block, BlockLike
from .entity import Entity
from .camera import Camera
from .events import Events

class Minecraft:
    def __init__(self, connection: Connection):
        self._conn = connection
        self.player = Player(self)
        self.entity = Entity(self)
        self.camera = Camera(self)
        self.events = Events(self)

    @classmethod
    def create(cls, host='127.0.0.1', port=4712, timeout=5):
        conn = Connection(host=host, port=port, timeout=timeout)
        return cls(conn)

    JSONPrimitive = Union[str, int, float, bool, None]
    JSONType = Union[JSONPrimitive, Dict[str, 'JSONType'], List['JSONType']]

    def _request(self, cmd: str, **kwargs) -> JSONType:
        payload = {
            'cmd': cmd,
            'args': kwargs
        }

        resp = self._conn.send(payload)

        if not isinstance(resp, dict):
            raise MinecraftProtocolError(
                'invalid response'
            )

        if resp.get('status') != 'ok':
            raise MinecraftProtocolError(
                resp.get('message') or 'error'
            )

        return resp.get('result', {})

    def postToChat(self, message: str) -> None:
        """Post a chat message to the server.

        Parameters
        ----------
        message : str
            Text to post in chat.

        Returns
        -------
        None
            The method performs an RPC and does not return a meaningful
            value on success.
        """
        self._request('postToChat', message=message)
        return None

    def setBlock(self, x: int, y: int, z: int, block: BlockLike, data: Optional[int] = None) -> None:
        """Set a single block. Accepts either:
        - a minecraft id string (e.g. 'minecraft:stone')
        - an int base id with optional `data` argument
        - a (base, data) tuple
        """
        block = Block(block, data)

        # Perform the request but do not return the raw server result to the
        # caller. If the bridge reports an error the call will raise a
        # MinecraftProtocolError; on success there is nothing meaningful to
        # return, so we return None.
        self._request('setBlock', x=x, y=y, z=z, block=block.name)
        return None

    def getBlock(self, x: int, y: int, z: int) -> Block:
        result = self._request(
            'getBlock',
            x=x,
            y=y,
            z=z
        )

        # result expected to be {"block": "minecraft:stone"} or similar
        if isinstance(result, dict):
            return Block(result)
        if isinstance(result, (str, int)):
            return Block(result)
        raise MinecraftProtocolError('unexpected getBlock response')

    def getBlocks(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int) -> List[Block]:
        res = self._request('getBlocks', x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1)
        # expect a flat list of block identifiers
        if not isinstance(res, list):
            raise MinecraftProtocolError('expected list from getBlocks')
        blocks: List[Block] = []
        for v in res:
            if isinstance(v, (str, int)) or isinstance(v, dict):
                blocks.append(Block(v))
            else:
                raise MinecraftProtocolError('unexpected element in getBlocks result')
        return blocks

    def setBlocks(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, block: BlockLike, data: Optional[int] = None) -> None:
        """Fill a rectangular area with a block.

        Parameters
        ----------
        x0, y0, z0, x1, y1, z1 : int
            Coordinates of the area corners.
        block : str|int|tuple
            Block specification accepted by :class:`Block`.
        data : int, optional
            Optional data/meta value.
        """
        block = Block(block, data)
        self._request('setBlocks', x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1, block=block.name)
        return None

    def getBlockWithData(self, x: int, y: int, z: int) -> Block:
        res = self._request('getBlockWithData', x=x, y=y, z=z)
        if isinstance(res, dict):
            return Block(res)
        if isinstance(res, (str, int)):
            return Block(res)
        raise MinecraftProtocolError('unexpected getBlockWithData response')

    def getHeight(self, x: int, z: int) -> int:
        res = self._request('getHeight', x=x, z=z)
        if isinstance(res, dict) and 'height' in res:
            val = res['height']
        else:
            val = res
        if isinstance(val, (int, float, str)):
            return int(val)
        raise MinecraftProtocolError('unexpected getHeight response')
