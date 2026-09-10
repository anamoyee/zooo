#!/usr/bin/env bash
# Run all configured paths through autosort.
# Default usage with no arguments provided, any arguments will be forwarded to the wrapped python arguably script

# === CONFIG ===

# relative to repo root
PATHS=(
    src/zooo/api/type/zoo.py
)

# === MACHINERY ===

fatal(){
	echo -- "$*" 1>&2;
	exit 1;
}

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || fatal "Failed to cd to script dir"
# cd repo root
UV=".venv/bin/uv"

for path in "${PATHS[@]}"; do
    "$UV" run ./tools/autosort.py "$path" "$@"
done
