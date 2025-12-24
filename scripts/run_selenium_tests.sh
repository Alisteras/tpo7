#!/bin/bash
cd ./reports
touch pytest_report.html
cd ./tests/selenium
python openbmc_auth_tests.py --html=../../reports/pytest_report.html
cd ../../
#!/bin/bash
