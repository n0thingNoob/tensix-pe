from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from tensixpe.ir.fabric import Fabric


class Backend(ABC):
    @abstractmethod
    def emit(self, fabric: Fabric, out_dir: str | Path) -> None: ...

    @abstractmethod
    def build(self, out_dir: str | Path) -> None: ...

    @abstractmethod
    def run(self, out_dir: str | Path, profile: bool = False) -> None: ...
