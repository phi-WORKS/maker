#!/usr/bin/env bash
# Synchronize project materials into FreeCAD's native User Material Library
# (~/.local/share/FreeCAD/v1-1/Material/maker/)
# Executes via the canonical run_freecad.sh runner.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

exec "${REPO_ROOT}/scripts/run_freecad.sh" "${REPO_ROOT}/src/phi_works/maker/materials/sync.py" "$@"
