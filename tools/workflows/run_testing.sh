#!/usr/bin/env bash

# uses the `pass` password manager to get cookie before running tests.
#
# USAGE: $0 [module]
#   ./tools/workflows/run_testing.sh             -> run all `testing`
#   ./tools/workflows/run_testing.sh {module}    -> run specific module, e.g. `./tools/workflows/run_testing.sh testing.client_lp`
#   PROFILING=1 ./tools/workflows/run_testing.sh -> run all or some tests with profiling

ZOOO_COOKIE=$(/usr/bin/env pass /dev/zooo/testing/cookie)

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || fatal "Failed to cd to script dir"
# cd repo root

if [ ! -e ".venv/bin/python3" ]; then
	fatal ".venv not found or corrupted. Please run uv sync."
fi

ZOOO_COOKIE="$ZOOO_COOKIE" .venv/bin/python3 -m "${@:-testing}"
