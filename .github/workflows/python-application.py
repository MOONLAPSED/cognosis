name: cognosis

on:
    push:
        branches: [ "main" ]
    pull_request:
        branches: [ "main" ]

jobs:

  setup:
    runs-on: ubuntu-latest

    steps:
        - name: Checkout code
        uses: actions/checkout@v2

        - name: Set up Python 3.10
        uses: actions/setup-python@v2
        with:
        python-version: "3.10"

  test:
    runs-on: ubuntu-latest
    steps:
        - name: Checkout code
        uses: actions/checkout@v2
        - name: Navigate to directory with main.py and print current directory
        run: cd /home/runner/work/cognosis/cognosis; pwd; ls -la

        - name: Test with pytest
        run: |
        python main.py 2>&1 | tee python-app.log > /dev/null || true  # Redirect both standard output and standard error to the python-app.log file

        - name: Archive test output as artifact
        if: always()
        uses: actions/upload-artifact@v2
        with:
        name: test-results
        path: test-output.txt
