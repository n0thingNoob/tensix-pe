#!/usr/bin/env bash
# Setup helper for the Ronin git submodule under external/ronin.
# This script never modifies anything inside external/ronin.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RONIN_DIR="$REPO_ROOT/external/ronin"
URL="${1:-}"

print_instructions() {
    cat <<EOF
external/ronin is not present yet.

To set it up as a git submodule, run one of:

  # preferred (your fork)
  git submodule add git@github.com:<your-username>/ronin.git external/ronin
  git submodule update --init --recursive

  # upstream fallback
  git submodule add git@github.com:tenstorrent/ronin.git external/ronin
  git submodule update --init --recursive

Or re-run this script with a URL:

  ./scripts/setup_ronin.sh git@github.com:<your-username>/ronin.git
EOF
}

is_populated() {
    [ -d "$RONIN_DIR" ] && [ -e "$RONIN_DIR/.git" ]
}

if is_populated; then
    echo "[setup_ronin] external/ronin already present at: $RONIN_DIR"
    echo "[setup_ronin] running: git submodule update --init --recursive"
    (cd "$REPO_ROOT" && git submodule update --init --recursive)
    exit 0
fi

if [ -n "$URL" ]; then
    echo "[setup_ronin] adding submodule from $URL -> external/ronin"
    (cd "$REPO_ROOT" && git submodule add "$URL" external/ronin)
    (cd "$REPO_ROOT" && git submodule update --init --recursive)
    echo "[setup_ronin] done. Ronin path: $RONIN_DIR"
    exit 0
fi

print_instructions
exit 0
