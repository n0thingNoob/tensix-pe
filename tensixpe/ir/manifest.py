from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def fabric_to_manifest_dict(fabric) -> dict[str, Any]:
    fabric.collect_streams_from_pes()

    inputs = {name: {"stream": s.name} for name, s in fabric.inputs.items()}
    outputs = {name: {"stream": s.name} for name, s in fabric.outputs.items()}
    pes = [pe.to_dict() for pe in fabric.pes]
    streams = [s.to_dict() for s in fabric.streams]

    return {
        "mesh": list(fabric.mesh),
        "inputs": inputs,
        "outputs": outputs,
        "pes": pes,
        "streams": streams,
    }


def write_manifest(fabric, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = fabric_to_manifest_dict(fabric)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
