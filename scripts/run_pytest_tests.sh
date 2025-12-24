#!/bin/bash

cd ./tests/pytest
pytest -v 
python3 -m pytest -v test_redfish.py 
cd ../../
#!/bin/bash
