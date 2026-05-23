"""Simple JSON-lines TCP connection for mcpi bridge.

This module provides a small, synchronous JSON-over-TCP helper used by
the :class:`mcpi.minecraft.Minecraft` client. It intentionally keeps
behavior minimal and raises specific exceptions for connection and
protocol errors.
"""

from __future__ import annotations

import socket
import json
from typing import Optional, TextIO

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4712
ENC = "utf-8"


class MinecraftConnectionError(Exception):
    """Raised for low-level connection errors."""


class MinecraftProtocolError(Exception):
    """Raised for protocol-level problems (invalid JSON, missing response)."""


class Connection:
    """A synchronous JSON-lines TCP connection for the bridge.

    Parameters
    ----------
    host : str
        Bridge host (defaults to ``127.0.0.1``).
    port : int
        Bridge port (defaults to ``4712``).
    timeout : float
        Socket connect timeout in seconds.
    """

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 5.0) -> None:
        self.host: str = host
        self.port: int = port
        self.timeout: float = float(timeout)
        self.sock: Optional[socket.socket] = None
        self.rfile: Optional[TextIO] = None
        self.wfile: Optional[TextIO] = None

    def open(self) -> None:
        """Open the underlying socket if not already open.

        Raises
        ------
        MinecraftConnectionError
            If the socket cannot be created or connected.
        """
        if self.sock:
            return
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self.rfile = self.sock.makefile('r', encoding=ENC)
            self.wfile = self.sock.makefile('w', encoding=ENC)
        except Exception as e:
            self.close()
            raise MinecraftConnectionError(str(e))

    def close(self) -> None:
        """Close the connection and associated file objects."""
        try:
            if self.rfile:
                self.rfile.close()
        finally:
            self.rfile = None
        try:
            if self.wfile:
                self.wfile.close()
        finally:
            self.wfile = None
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.sock = None

    def send(self, obj: object, expect_response: bool = True) -> Optional[object]:
        """Send a Python object as JSON and optionally wait for a response.

        Parameters
        ----------
        obj : object
            JSON-serializable payload to send.
        expect_response : bool
            When ``True`` read and parse a single-line JSON response.

        Returns
        -------
        object | None
            The parsed JSON response (usually a ``dict``) or ``None`` when
            no response is expected.

        Raises
        ------
        MinecraftProtocolError
            When the response cannot be parsed or no response is received.
        MinecraftConnectionError
            For underlying socket errors.
        """
        self.open()
        try:
            line = json.dumps(obj, ensure_ascii=False)
            # ensure the file objects are present (open() should have created them)
            assert self.wfile is not None and self.rfile is not None
            self.wfile.write(line + "\n")
            self.wfile.flush()
            if not expect_response:
                return None
            resp_line = self.rfile.readline()
            if not resp_line:
                raise MinecraftProtocolError("no response from server")
            return json.loads(resp_line)
        except json.JSONDecodeError as e:
            raise MinecraftProtocolError(str(e))
        except Exception as e:
            self.close()
            raise MinecraftConnectionError(str(e))
