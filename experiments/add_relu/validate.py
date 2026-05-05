"""Placeholder. Future: compare generated output against CPU reference and
the manual Tanto baseline (numerical diff per tile)."""
from __future__ import annotations


def main() -> None:
    print("validate.py: TODO")
    print("  - run generated Tanto code (fused + split) under Jitte")
    print("  - run manual Tanto baseline (fused + split) under Jitte")
    print("  - compute CPU reference for C = relu(A + B)")
    print("  - assert max|generated - reference| ~= 0")
    print("  - assert generated and manual baseline match bit-for-bit")


if __name__ == "__main__":
    main()
