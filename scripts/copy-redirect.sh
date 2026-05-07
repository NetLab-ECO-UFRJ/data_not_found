#!/usr/bin/env bash
set -euo pipefail
SRC="$(dirname "$0")/../redirect.html"
DEST="$(dirname "$0")/../_output/index.html"
mkdir -p "$(dirname "$DEST")"
cp "$SRC" "$DEST"
echo "Installed language redirect at $DEST"
