#! /usr/bin/env bash

set -x
echo -e "\nStart black:"
black app --check

echo -e "\nStart flake8:"
flake8 --show-source