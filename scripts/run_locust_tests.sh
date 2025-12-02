#!/bin/bash

cd ./reports
touch locust_report.html
cd ../
cd ./tests/locust
rm -rf locust_env
python3 -m venv locust_env
source locust_env/bin/activate
pip install -r requirements.txt
locust -f openbmc_test.py --headless \
    --users 10 \
    --spawn-rate 2 \
    --run-time 30s \
    --host=https://localhost:2443 \
    --html=../../reports/locust_report.html
cd ../../