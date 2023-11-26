#!/bin/bash
set -e

echo "Running mypy..."
mypy cognosis

echo "Running bandit..."
bandit -c pyproject.toml -r cognosis
