#!/bin/bash

# Format with black
echo "Running black..."
black . --exclude "venv/|\.pytest_cache/|\.mypy_cache/|__pycache__/|build/|dist/"

# Sort imports
echo "Running isort..."
isort . --skip-glob "*cache*" --skip-glob "*.pyc" --skip-glob "build/*" --skip-glob "dist/*" --skip venv

# Run flake8
echo "Running flake8..."
flake8 . --exclude=venv,__pycache__,.pytest_cache,.mypy_cache,build,dist

# Check for type hints
echo "Running mypy..."
mypy anki_vocab_builder --exclude '(build|dist|venv|\.pytest_cache|\.mypy_cache|__pycache__)' 