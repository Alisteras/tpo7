#!/bin/bash
cd ./reports
touch pytest_report.html
cd ../
cd ./tests/pytest
pytest -v 
python3 -m pytest -v test_redfish.py  --html=../../reports/pytest_report.html
cd ../../
#!/bin/bash
