from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tensixpe.ir.stream import TileStream


@dataclass
class TensixPE:
    name: str
    pe_type: str
    coord: tuple[int, int] | None = None
    params: dict[str, Any] = field(default_factory=dict)
    inputs: list[TileStream] = field(default_factory=list)
    outputs: list[TileStream] = field(default_factory=list)

    def _make_output(self, idx: int = 0) -> TileStream:
        return TileStream(name=f"{self.name}_out{idx}", src=self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.pe_type,
            "coord": list(self.coord) if self.coord is not None else None,
            "params": dict(self.params),
        }


class FpuPE(TensixPE):
    def __init__(self, name: str, op: str = "add", coord=None, **params):
        super().__init__(
            name=name,
            pe_type="FpuPE",
            coord=coord,
            params={"op": op, **params},
        )

    def __call__(self, a: TileStream, b: TileStream) -> TileStream:
        a.dst = self
        b.dst = self
        self.inputs = [a, b]
        out = self._make_output(0)
        self.outputs = [out]
        return out


class SfpuPE(TensixPE):
    def __init__(self, name: str, op: str = "relu", coord=None, **params):
        super().__init__(
            name=name,
            pe_type="SfpuPE",
            coord=coord,
            params={"op": op, **params},
        )

    def __call__(self, x: TileStream) -> TileStream:
        x.dst = self
        self.inputs = [x]
        out = self._make_output(0)
        self.outputs = [out]
        return out


class FpuSfpuPE(TensixPE):
    def __init__(
        self,
        name: str,
        fpu_op: str = "add",
        sfpu_op: str = "relu",
        coord=None,
        **params,
    ):
        super().__init__(
            name=name,
            pe_type="FpuSfpuPE",
            coord=coord,
            params={"fpu_op": fpu_op, "sfpu_op": sfpu_op, **params},
        )

    def __call__(self, a: TileStream, b: TileStream) -> TileStream:
        a.dst = self
        b.dst = self
        self.inputs = [a, b]
        out = self._make_output(0)
        self.outputs = [out]
        return out
