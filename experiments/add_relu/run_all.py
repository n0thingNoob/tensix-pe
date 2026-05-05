"""Regenerate the two examples and verify the expected file layout."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


FUSED_OUT = REPO_ROOT / "generated/tanto/add_relu_fused"
SPLIT_OUT = REPO_ROOT / "generated/tanto/add_relu_split"

FUSED_EXPECTED = [
    "manifest.yaml",
    "host.cpp",
    "kernels/PE0_fpu_sfpu_pe.cpp",
    "build.sh",
    "run_jitte.sh",
]
SPLIT_EXPECTED = [
    "manifest.yaml",
    "host.cpp",
    "kernels/FPU0_fpu_pe.cpp",
    "kernels/SFPU0_sfpu_pe.cpp",
    "build.sh",
    "run_jitte.sh",
]
BASELINE_DIRS = [
    REPO_ROOT / "baselines/tanto_manual/add_relu_fused",
    REPO_ROOT / "baselines/tanto_manual/add_relu_split",
]


def _run_example(rel_path: str) -> None:
    script = REPO_ROOT / rel_path
    print(f"=== running {rel_path} ===", flush=True)
    subprocess.run([sys.executable, str(script)], check=True)


def _check(label: str, missing: list[Path]) -> bool:
    if not missing:
        print(f"PASS  {label}")
        return True
    print(f"FAIL  {label}")
    for m in missing:
        print(f"        missing: {m}")
    return False


def main() -> int:
    _run_example("examples/add_relu_fused_pe.py")
    _run_example("examples/add_relu_split_pe.py")

    fused_missing = [FUSED_OUT / f for f in FUSED_EXPECTED if not (FUSED_OUT / f).exists()]
    split_missing = [SPLIT_OUT / f for f in SPLIT_EXPECTED if not (SPLIT_OUT / f).exists()]
    fused_baseline_missing = [] if BASELINE_DIRS[0].is_dir() else [BASELINE_DIRS[0]]
    split_baseline_missing = [] if BASELINE_DIRS[1].is_dir() else [BASELINE_DIRS[1]]

    print("=== summary ===")
    ok = True
    ok &= _check("generated fused files", fused_missing)
    ok &= _check("generated split files", split_missing)
    ok &= _check("manual fused baseline", fused_baseline_missing)
    ok &= _check("manual split baseline", split_baseline_missing)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
