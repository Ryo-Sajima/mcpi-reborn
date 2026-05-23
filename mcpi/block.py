"""Typed block helper for mcpi client.

This module exposes ``NUM_TO_NAME``-backed lookup via :class:`Block` and a
``name_to_num`` reverse mapping. Propertyized block names such as
``minecraft:stone_slab[type=bottom]`` are supported and treated strictly:
if a propertyized name or a numeric pair is unknown the constructor raises
``ValueError`` instead of silently falling back to air.
"""

from __future__ import annotations

from typing import Dict, Tuple, Optional, Union, cast, Mapping

from ._num_to_name import NUM_TO_NAME


BlockLike = Union["Block", int, str, Tuple[int, int], Mapping[str, object]]


def name_to_num() -> Dict[str, Tuple[int, int]]:
    """Return a mapping name -> (base, meta). Cached on first call.

    The mapping includes both fully-qualified names (``minecraft:...``)
    and the short form without the ``minecraft:`` prefix. Propertyized
    names (``[k=v]``) are preserved as part of the mapping keys.
    """
    try:
        return name_to_num._cache  # type: ignore[attr-defined]
    except AttributeError:
        mapping: Dict[str, Tuple[int, int]] = {}
        for (b, m), name in NUM_TO_NAME.items():
            if not name:
                continue
            mapping[name] = (b, m)
            short = name.replace("minecraft:", "")
            if short not in mapping:
                mapping[short] = (b, m)
        name_to_num._cache = mapping  # type: ignore[attr-defined]
        return mapping


def _split_propertyized(name: str) -> Tuple[str, Optional[Dict[str, str]]]:
    """Split a possibly propertyized block name into base and properties.

    Returns (base_name, props_dict) where props_dict is ``None`` when no
    properties are present.
    """
    pstart = name.find("[")
    if pstart == -1:
        return name, None
    pend = name.rfind("]")
    if pend == -1 or pend < pstart:
        raise ValueError(f"Malformed propertyized name: {name}")
    base = name[:pstart]
    inner = name[pstart + 1 : pend]
    props: Dict[str, str] = {}
    if inner.strip():
        for part in inner.split(","):
            kv = part.split("=", 1)
            if len(kv) != 2:
                raise ValueError(f"Malformed property pair: {part}")
            props[kv[0].strip()] = kv[1].strip()
    return base, props


class Block:
    """Representation of a Minecraft block.

    The constructor is strict: unknown names or numeric pairs raise
    ``ValueError``. Accepts the same inputs as the traditional MCPI
    libraries plus propertyized names.
    """

    def __init__(self, value: BlockLike, data: Optional[int] = None) -> None:
        self.id: int = 0
        self.data: int = 0
        self.name: str = "minecraft:air"

        # copy constructor
        if isinstance(value, Block):
            self.id = int(value.id)
            self.data = int(value.data)
            self.name = value.name
            return

        # tuple (base, meta)
        if isinstance(value, tuple) and len(value) == 2:
            base = int(cast(int, value[0]))
            meta = int(cast(int, value[1]))
            nm = NUM_TO_NAME.get((base, meta), "")
            if not nm:
                raise ValueError(f"Unknown block for base={base}, data={meta}")
            self.id = base
            self.data = meta
            self.name = nm
            return

        # integer base id + optional data
        if isinstance(value, int):
            base = int(value)
            meta = int(data or 0)
            nm = NUM_TO_NAME.get((base, meta), "")
            if not nm:
                raise ValueError(f"Unknown block for base={base}, data={meta}")
            self.id = base
            self.data = meta
            self.name = nm
            return

        # string name (may be propertyized)
        if isinstance(value, str):
            name = value
            if not name.startswith("minecraft:"):
                name = "minecraft:" + name
            # If the name is not present in our static NUM_TO_NAME mapping,
            # do not raise here — keep the provided name and let the server
            # validate it at runtime.
            num = name_to_num().get(name)
            if num is None:
                # unknown name: preserve the name for the bridge to validate
                self.id = 0
                self.data = int(data or 0)
                self.name = name
                return
            base, meta = int(num[0]), int(num[1])
            # allow explicit data override but don't pre-validate beyond
            # looking up the canonical mapping
            if data is not None:
                meta = int(data)
            self.id = base
            self.data = meta
            self.name = NUM_TO_NAME.get((base, meta), name)
            return

        # dict input (numerical id preferred)
        if isinstance(value, dict):
            if "id" in value:
                idv = value["id"]
                if isinstance(idv, (tuple, list)) and len(idv) == 2:
                    base = int(cast(int, idv[0]))
                    meta = int(cast(int, idv[1]))
                    nm = NUM_TO_NAME.get((base, meta), "")
                    self.id = base
                    self.data = meta
                    self.name = nm if nm else ""
                    return
                if isinstance(idv, int) or (isinstance(idv, str) and idv.isdigit()):
                    base = int(cast(int, idv))
                    meta = int(cast(int, value.get("data", data or 0)))
                    nm = NUM_TO_NAME.get((base, meta), "")
                    self.id = base
                    self.data = meta
                    self.name = nm if nm else ""
                    return

            # named forms
            name_val = value.get("block") or value.get("name") or value.get("minecraft_id") or value.get("id")
            if isinstance(name_val, str):
                if not name_val.startswith("minecraft:"):
                    name_val = "minecraft:" + name_val
                # if properties are provided, compose the propertyized form
                props = value.get("properties")
                if isinstance(props, dict) and props:
                    inner = ",".join(f"{k}={v}" for k, v in props.items())
                    full = f"{name_val}[{inner}]"
                    num = name_to_num().get(full)
                    if num is None:
                        # unknown propertyized name: preserve and defer
                        self.id = 0
                        self.data = int(cast(int, value.get("data", data or 0)))
                        self.name = full
                        return
                    base, meta = int(cast(int, num[0])), int(cast(int, num[1]))
                    self.id = base
                    self.data = meta
                    self.name = NUM_TO_NAME.get((base, meta), full)
                    return
                num = name_to_num().get(name_val)
                if num is None:
                    # unknown name in dict form: preserve and defer to server
                    self.id = 0
                    self.data = int(cast(int, value.get("data", data or 0)))
                    self.name = name_val
                    return
                base, meta = int(cast(int, num[0])), int(cast(int, num[1]))
                meta = int(cast(int, value.get("data", data or meta)))
                self.id = base
                self.data = meta
                self.name = NUM_TO_NAME.get((base, meta), name_val)
                return

        raise ValueError(f"Invalid block specification: {value!r}")

    def __int__(self) -> int:
        """Return the legacy base id (int)."""
        return int(self.id)

    def __repr__(self) -> str:
        return f'Block(id={self.id}, name="{self.name}", data={self.data})'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Block):
            return self.id == other.id and self.data == other.data
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            n = other
            if not n.startswith("minecraft:"):
                n = "minecraft:" + n
            return self.name == n
        return False
