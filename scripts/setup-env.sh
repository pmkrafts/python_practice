#!/usr/bin/env bash
set -euo pipefail

echo "🐍 Python Backend + AI Agent Coding Practice — Environment Setup"

# Check Python version
if ! command -v python3 &>/dev/null; then
    echo "❌ python3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install uv if not present
if ! command -v uv &>/dev/null; then
    echo "📦 Installing uv..."
    pip install uv
fi

# Install dependencies
if [ -f "pyproject.toml" ]; then
    echo "📦 Installing dependencies via uv..."
    uv sync --all-extras
else
    echo "📦 Installing dependencies via pip..."
    pip install -r requirements.txt
fi

# Install pre-commit hooks
if command -v pre-commit &>/dev/null; then
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
fi

# Create .env from example if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

echo "✅ Setup complete. Activate the environment with: source .venv/bin/activate"
