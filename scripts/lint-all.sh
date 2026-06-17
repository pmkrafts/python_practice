#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Running linters and type checks..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

echo "🔍 Running ruff check..."
ruff check .

echo "🔍 Running ruff format check..."
ruff format --check .

echo "🔍 Running mypy..."
mypy common

echo "✅ Linting and type checks passed"
