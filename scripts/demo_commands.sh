#!/usr/bin/env bash
# Demo helper for macOS/Linux
set -euo pipefail

python app.py get-all || true

python app.py add --first "Alice" --last "Wonder" --email "alice.wonder@example.com" --date 2023-09-03 || true

python app.py update-email --id 1 --email "johnny.doe@example.com" || true

python app.py delete --id 2 || true

python app.py get-all || true
