#!/bin/bash
cd ./reports
touch pytest_report.html
cd ../
cd ./tests/pytest
rm -rf pytest_env
python3 -m venv pytest_env
source pytest_env/bin/activate
pip install -r requirements.txt
pytest -v 
python3 -m pytest -v test_redfish.py  --html=../../reports/pytest_report.html
cd ../../
#!/bin/bash
