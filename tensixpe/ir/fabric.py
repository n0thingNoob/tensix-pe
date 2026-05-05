from __future__ import annotations

from pathlib import Path
from typing import Any

from tensixpe.ir.pe import TensixPE
from tensixpe.ir.stream import TileStream


class Fabric:
    def __init__(self, mesh: tuple[int, int]):
        self.mesh: tuple[int, int] = tuple(mesh)
        self.inputs: dict[str, TileStream] = {}
        self.outputs: dict[str, TileStream] = {}
        self.pes: list[TensixPE] = []
        self.streams: list[TileStream] = []

    def input(self, name: str) -> TileStream:
        s = TileStream(name=name, src=f"dram.{name}")
        self.inputs[name] = s
        self.add_stream(s)
        return s

    def output(self, name: str, stream: TileStream) -> None:
        stream.dst = f"dram.{name}"
        self.outputs[name] = stream
        self.add_stream(stream)

    def place(self, pe: TensixPE, coord: tuple[int, int]) -> TensixPE:
        pe.coord = tuple(coord)
        self.pes.append(pe)
        return pe

    def add_stream(self, stream: TileStream) -> None:
        for s in self.streams:
            if s.name == stream.name:
                return
        self.streams.append(stream)

    def collect_streams_from_pes(self) -> None:
        for pe in self.pes:
            for s in pe.inputs:
                self.add_stream(s)
            for s in pe.outputs:
                self.add_stream(s)

    def to_manifest_dict(self) -> dict[str, Any]:
        from tensixpe.ir.manifest import fabric_to_manifest_dict
        return fabric_to_manifest_dict(self)

    def to_manifest(self, path: str | Path) -> None:
        from tensixpe.ir.manifest import write_manifest
        write_manifest(self, path)
