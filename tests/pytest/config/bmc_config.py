import os
from dataclasses import dataclass

@dataclass
class BmcCredentials:
    login: str
    password: str

class BmcConfig:
    BMC_IP = os.getenv('BMC_IP', 'localhost:2443')
    BASE_URL = f"https://{BMC_IP}"
    
    credentials = BmcCredentials(
        login=os.getenv('BMC_USER', 'root'),
        password=os.getenv('BMC_PASSWORD', '0penBmc')
    )
