from locust import HttpUser, task, between
import base64
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBMCUser(HttpUser):
    host = "https://localhost:2443"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.verify = False
        self.auth_header = {
            "Authorization": "Basic " + base64.b64encode(b"root:0penBmc").decode("utf-8")
        }

    @task(3)
    def get_system_info(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            headers=self.auth_header,
            name="BMC_System_Info"
        )

    @task(2)
    def get_power_state(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            headers=self.auth_header,
            name="BMC_Power_State"
        )