#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py38-plus --recursive cognosis tests

echo "Running ruff..."
ruff cognosis tests --fix

echo "Running black..."
black cognosis tests
