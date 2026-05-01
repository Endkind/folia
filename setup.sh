#!/bin/bash

set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip

echo "Installing pre-commit and setting up hooks..."
pip install pre-commit
pre-commit install

if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
fi

echo "Dependencies installed and pre-commit hooks configured."
