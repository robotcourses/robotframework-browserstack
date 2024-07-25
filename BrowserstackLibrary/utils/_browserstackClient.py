import requests
import requests.auth
from robot.api.deco import not_keyword

class _BrowserstackClient:
    def __init__(self, auth_user, auth_token):
        self.auth = (auth_user, auth_token)
        self.base_url = "https://api-cloud.browserstack.com/app-automate"

    @not_keyword
    def browserstack_request(self, endpoint, method, data=None, files=None):
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': requests.auth._basic_auth_str(*self.auth)}
        if files:
            response = requests.request(method, url, headers=headers, data=data, files=files)
        else:
            headers['Content-Type']='application/json'
            response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()