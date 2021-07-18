#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

# We should be in this folder, otherwise an error will be thrown
cd ./pyfriends

echo "Running notebooks through ipython 👀"
ipython -c "%run build_integration_layer.ipynb"
