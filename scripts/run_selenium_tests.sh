#!/bin/bash

cd ./reports
touch selenium_report.html
cd ../
cd ./tests/selenium
rm -rf selenium_env
python3 -m venv selenium_env
source selenium_env/bin/activate
pip install -r requirements.txt
python openbmc_auth_tests.py  --html=../../reports/locust_report.html
cd ../../
#!/bin/bash
