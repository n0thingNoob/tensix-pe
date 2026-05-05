#!/usr/bin/env bash
# Remove generated Tanto outputs, preserving .gitkeep files.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for d in \
    "$REPO_ROOT/generated/tanto/add_relu_fused" \
    "$REPO_ROOT/generated/tanto/add_relu_split"; do
    if [ -d "$d" ]; then
        echo "[clean_generated] removing $d"
        rm -rf "$d"
    fi
done

echo "[clean_generated] done. .gitkeep files preserved."
