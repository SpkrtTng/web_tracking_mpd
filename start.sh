#!/bin/bash

# Exit early on errors
set -eu

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

# Python version to use
PYTHON_VERSION=python3.10

# Check if python3.10 is available
if ! command -v $PYTHON_VERSION &> /dev/null; then
  echo "$PYTHON_VERSION could not be found"
  exit 1
fi

# Install Python 3 virtual env
VIRTUALENV=.data/venv

if [ ! -d $VIRTUALENV ]; then
  $PYTHON_VERSION -m venv $VIRTUALENV
fi

if [ ! -f $VIRTUALENV/bin/pip ]; then
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
fi

# Install the requirements
$VIRTUALENV/bin/pip install google-cloud-bigquery==3.23.1

# Check if run.py exists
if [ ! -f run.py ]; then
  echo "run.py not found"
  exit 1
fi

# Run a glorious Python 3 server
$VIRTUALENV/bin/python run.py
