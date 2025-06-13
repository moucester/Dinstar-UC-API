import requests
import json
from requests.auth import HTTPDigestAuth

class DinstarUC:
    """
    Base class for interacting with the Dinstar API.
    This class handles authentication and sending HTTP requests.
    """

    def __init__(self, username, password, gateway_url, verify_ssl=True):
        """
        Initialize the DinstarUC class with authentication details.
        :param username: API username.
        :param password: API password.
        :param gateway_url: Base URL of the Dinstar gateway.
        :param verify_ssl: Whether to verify SSL certificates (default: True).
        """
        self.username = username
        self.password = password
        self.gateway_url = gateway_url
        self.verify_ssl = verify_ssl

    def send_request(self, endpoint, data):
        """
        Send an authenticated request to the Dinstar API.
        :param endpoint: API endpoint to send the request to.
        :param data: Dictionary containing request payload.
        :return: JSON response from the API.
        """
        url = f"{self.gateway_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                url,
                auth=HTTPDigestAuth(self.username, self.password),
                headers=headers,
                data=json.dumps(data),
                verify=self.verify_ssl  # SSL verification is configurable
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}