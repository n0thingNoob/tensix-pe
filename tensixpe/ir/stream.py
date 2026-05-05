from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TileStream:
    name: str
    src: str | object | None = None
    dst: str | object | None = None
    dtype: str = "bfloat16"
    tile_shape: tuple[int, int] = (32, 32)
    transport: str = "pipe"
    buffering: int = 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "src": _name_of(self.src),
            "dst": _name_of(self.dst),
            "dtype": self.dtype,
            "tile_shape": list(self.tile_shape),
            "transport": self.transport,
            "buffering": self.buffering,
        }


def _name_of(x: Any) -> str | None:
    if x is None:
        return None
    if isinstance(x, str):
        return x
    return getattr(x, "name", str(x))
