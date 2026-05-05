"""Generated example: C = relu(A + B), fused on a single FpuSfpuPE."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tensixpe import Fabric, FpuSfpuPE
from tensixpe.backends.tanto import TantoBackend


def main() -> Path:
    fabric = Fabric(mesh=(8, 8))

    A = fabric.input("A")
    B = fabric.input("B")

    pe0 = fabric.place(
        FpuSfpuPE("PE0", fpu_op="add", sfpu_op="relu"),
        coord=(0, 0),
    )

    C = pe0(A, B)
    fabric.output("C", C)

    out_dir = REPO_ROOT / "generated/tanto/add_relu_fused"
    backend = TantoBackend(ronin_home="external/ronin")
    backend.emit(fabric, out_dir)

    print(f"Generated: {out_dir}")
    return out_dir


if __name__ == "__main__":
    main()
