import requests
import json
from requests.auth import HTTPDigestAuth
from typing import Optional

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

    def send_request(self, endpoint, data=None, method="POST"):
        """
        Send an authenticated HTTP request to the Dinstar API.

        Args:
            endpoint (str): API endpoint to send the request to.
            data (dict or None): Request payload for POST or query params for GET.
            method (str): HTTP method, either 'GET' or 'POST'. Defaults to 'POST'.

        Returns:
            dict: Parsed JSON response from the API, or error information on failure.
        """
        url = f"{self.gateway_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            if method.upper() == "GET":
                response = requests.get(
                    url,
                    auth=HTTPDigestAuth(self.username, self.password),
                    headers=headers,
                    params=data,
                    verify=self.verify_ssl
                )
            elif method.upper() == "POST":
                if isinstance(data, str):
                    body = data
                else:
                    body = json.dumps(data) if data else None
                response = requests.post(
                    url,
                    auth=HTTPDigestAuth(self.username, self.password),
                    headers=headers,
                    data=body,
                    verify=self.verify_ssl
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # Optionally log the error here
            print(f"Request to {url} failed: {e}")
            return {"error": str(e)}

    def send_raw_request(self, endpoint: str, data: Optional[any], method: str = "POST") -> Optional[requests.Response]:
        """
        Send an authenticated HTTP request to the Dinstar API and return the full Response object.

        Args:
            endpoint (str): API endpoint to send the request to (e.g., "/api/get_status").
            data (any, optional): Payload data to send with the request. Should be JSON serializable.
            method (str): HTTP method to use. Defaults to "POST".

        Returns:
            requests.Response: The full HTTP response object on success.
            None: If a request exception occurs.

        Notes:
            - SSL verification is configurable via self.verify_ssl.
            - Exceptions are caught and logged internally; consider enhancing error handling as needed.
        """
        url = f"{self.gateway_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.request(
                method=method,
                url=url,
                auth=HTTPDigestAuth(self.username, self.password),
                headers=headers,
                data=json.dumps(data) if data is not None else None,
                verify=self.verify_ssl
            )
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
            return response
        except requests.exceptions.RequestException as e:
            # You can log the error here if you want
            print(f"Request to {url} failed: {e}")
            return None