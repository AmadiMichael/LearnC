#!/usr/bin/env bash
# Run from anywhere: tests for K&R exercises 1-20 through 1-24, 2-1 through 2-10, 3-1 through 3-6, and 4-1 through 4-13.
# Usage: ./tests/run.sh [20|21|22|23|24|2-1|2-2|2-3|2-4|2-5|2-6|2-7|2-8|2-9|2-10|3-1|3-2|3-3|3-4|3-5|3-6|4-1|4-2|4-3|4-4|4-5|4-6|4-7|4-8|4-10|4-11|4-12|4-13] ...
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/tests/helpers/run_tests.py" "$@"
