"""Generated example: Y = A + B; C = relu(Y) — split across two PEs."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tensixpe import Fabric, FpuPE, SfpuPE
from tensixpe.backends.tanto import TantoBackend


def main() -> Path:
    fabric = Fabric(mesh=(8, 8))

    A = fabric.input("A")
    B = fabric.input("B")

    fpu = fabric.place(FpuPE("FPU0", op="add"), coord=(0, 0))
    sfpu = fabric.place(SfpuPE("SFPU0", op="relu"), coord=(0, 1))

    Y = fpu(A, B)
    C = sfpu(Y)

    fabric.output("C", C)

    out_dir = REPO_ROOT / "generated/tanto/add_relu_split"
    backend = TantoBackend(ronin_home="external/ronin")
    backend.emit(fabric, out_dir)

    print(f"Generated: {out_dir}")
    return out_dir


if __name__ == "__main__":
    main()
