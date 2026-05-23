"""Utility exceptions shared by MCPI client modules."""


class MinecraftConnectionError(Exception):
    """Raised for low-level connection errors in the MCPI bridge client."""


class MinecraftProtocolError(Exception):
    """Raised for protocol-level problems such as invalid JSON responses."""
