from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from tensixpe.ir.fabric import Fabric
from tensixpe.ir.pe import TensixPE, FpuPE, SfpuPE, FpuSfpuPE

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


def render_template(template_name: str, context: dict[str, Any], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = _env.get_template(template_name).render(**context)
    out_path.write_text(text)


def _kernel_template_for(pe: TensixPE) -> tuple[str, str]:
    if isinstance(pe, FpuSfpuPE):
        return "fpu_sfpu_pe.cpp.j2", f"{pe.name}_fpu_sfpu_pe.cpp"
    if isinstance(pe, FpuPE):
        return "fpu_pe.cpp.j2", f"{pe.name}_fpu_pe.cpp"
    if isinstance(pe, SfpuPE):
        return "sfpu_pe.cpp.j2", f"{pe.name}_sfpu_pe.cpp"
    raise TypeError(f"No Tanto kernel template for PE type {type(pe).__name__}")


def _fabric_context(fabric: Fabric, project_name: str, ronin_home: str) -> dict[str, Any]:
    return {
        "project_name": project_name,
        "ronin_home": ronin_home,
        "mesh": list(fabric.mesh),
        "inputs": [{"name": n, "stream": s.name} for n, s in fabric.inputs.items()],
        "outputs": [{"name": n, "stream": s.name} for n, s in fabric.outputs.items()],
        "pes": [
            {
                "name": pe.name,
                "type": type(pe).__name__,
                "coord": list(pe.coord) if pe.coord else [0, 0],
                "params": dict(pe.params),
                "inputs": [s.name for s in pe.inputs],
                "outputs": [s.name for s in pe.outputs],
            }
            for pe in fabric.pes
        ],
        "streams": [s.to_dict() for s in fabric.streams],
    }


def emit_host(fabric: Fabric, out_dir: Path, project_name: str, ronin_home: str) -> None:
    ctx = _fabric_context(fabric, project_name, ronin_home)
    render_template("host.cpp.j2", ctx, out_dir / "host.cpp")


def emit_kernel(pe: TensixPE, out_dir: Path) -> None:
    template, filename = _kernel_template_for(pe)
    ctx = {
        "pe_name": pe.name,
        "pe_type": type(pe).__name__,
        "params": dict(pe.params),
        "fpu_op": pe.params.get("fpu_op") or pe.params.get("op", "add"),
        "sfpu_op": pe.params.get("sfpu_op") or pe.params.get("op", "relu"),
        "tile_shape": [32, 32],
    }
    render_template(template, ctx, out_dir / "kernels" / filename)


def emit_scripts(fabric: Fabric, out_dir: Path, project_name: str, ronin_home: str) -> None:
    ctx = {"project_name": project_name, "ronin_home": ronin_home}
    build_path = out_dir / "build.sh"
    run_path = out_dir / "run_jitte.sh"
    render_template("build.sh.j2", ctx, build_path)
    render_template("run_jitte.sh.j2", ctx, run_path)
    os.chmod(build_path, 0o755)
    os.chmod(run_path, 0o755)
