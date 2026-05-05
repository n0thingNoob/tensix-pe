from __future__ import annotations

from pathlib import Path

from tensixpe.backends.base import Backend
from tensixpe.backends.tanto.emit import emit_host, emit_kernel, emit_scripts
from tensixpe.ir.fabric import Fabric
from tensixpe.ir.manifest import write_manifest


class TantoBackend(Backend):
    def __init__(self, ronin_home: str | Path = "external/ronin"):
        self.ronin_home = str(ronin_home)

    def emit(self, fabric: Fabric, out_dir: str | Path) -> None:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "kernels").mkdir(parents=True, exist_ok=True)

        project_name = out_dir.name

        write_manifest(fabric, out_dir / "manifest.yaml")
        emit_host(fabric, out_dir, project_name, self.ronin_home)
        for pe in fabric.pes:
            emit_kernel(pe, out_dir)
        emit_scripts(fabric, out_dir, project_name, self.ronin_home)

    def build(self, out_dir: str | Path) -> None:
        out_dir = Path(out_dir)
        print(f"[tanto] would build: bash {out_dir / 'build.sh'}")
        print(f"[tanto] (TODO: real Ronin/Tanto build using {self.ronin_home})")

    def run(self, out_dir: str | Path, profile: bool = False) -> None:
        out_dir = Path(out_dir)
        print(f"[tanto] would run: bash {out_dir / 'run_jitte.sh'}")
        if profile:
            print("[tanto] (TODO: profiling not yet supported in MVP)")
        print(f"[tanto] (TODO: real Jitte run using {self.ronin_home})")
