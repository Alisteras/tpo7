#!/bin/bash

cd ./tests/pytest
pytest -v
python3 -m pytest -v test_redfish.py > test_redfish.txt 2>&1
cd ../../
