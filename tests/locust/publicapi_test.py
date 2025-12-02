from locust import HttpUser, task, between
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PublicAPIUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        self.client.get("/posts", name="JSONPlaceholder_Posts")