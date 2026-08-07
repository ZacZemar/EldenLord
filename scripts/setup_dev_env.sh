#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

echo ""
echo "Development environment ready."
echo "Activate it with:"
echo "source .venv/bin/activate"