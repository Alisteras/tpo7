#!/bin/bash
cd ./reports
touch selenium_report.html
cd ./tests/selenium
python openbmc_auth_tests.py --html=../../reports/selenium_report.html
cd ../../
#!/bin/bash
