#!/bin/bash

echo $(ruff --config ruff.toml check --select I --fix .)
echo $(ruff --config ruff.toml format --line-length 88 .)
