from typing import Any, Optional

import requests


class NSORestconfClient:
    """
    A client for interacting with the NSO RESTCONF API.

    Attributes:
        base_url (str): The base URL for the RESTCONF API.
        session (requests.Session): The requests session used for making HTTP calls.
    """

    _DATA_PATH = "/data"

    def __init__(
        self,
        scheme: str = "http",
        address: str = "localhost",
        port: int = 8080,
        timeout: int = 30,
        username: Optional[str] = None,
        password: Optional[str] = None,
        disable_warning: bool = False,
    ) -> None:
        """
        Initializes the NSORestconfClient.

        Args:
            scheme (str): The URL scheme (http or https). Defaults to "http".
            address (str): The address of the NSO server. Defaults to "localhost".
            port (int): The port on which the NSO server is listening. Defaults to 8080.
            username (Optional[str]): The username for authentication. Defaults to None.
            password (Optional[str]): The password for authentication. Defaults to None.
            timeout (int): The timeout (seconds) of the requests session. Defaults to 30 seconds.
            disable_warning (bool): Whether to disable SSL certificate warnings. Defaults to False.
        """
        self.timeout = timeout

        self.base_url = f"{scheme}://{address}:{port}/restconf"
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update(
            {
                "Content-Type": "application/yang-data+json",
                "Accept": "application/yang-data+json",
            }
        )

        # Disable warning for self-signed certificates
        if disable_warning:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get(self, resource: str) -> Any:
        """
        Sends a GET request to the specified RESTCONF resource.

        Args:
            resource (str): The resource path to fetch from the RESTCONF API.

        Returns:
            Any: The response data in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}/{self._DATA_PATH}/{resource}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Other error occurred: {err}")

    def close(self) -> None:
        """
        Closes the HTTP session.
        """
        self.session.close()
