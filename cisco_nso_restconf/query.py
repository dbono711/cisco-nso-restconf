from typing import Any, Dict

from .client import NSORestconfClient
import json


class Query:
    """
    A helper class for interacting with the Cisco NSO 'tailf-ncs:query' resource via RESTCONF.

    This class provides methods to interact with query-related resources in Cisco NSO,
    using the `NSORestconfClient` to perform underlying REST operations.
    """

    def __init__(self, client: NSORestconfClient):
        """
        Initializes the Query helper class.

        Args:
            client (NSORestconfClient): An instance of NSORestconfClient used to send RESTCONF requests.
        """
        self.client = client

    def query_device_platform(self) -> Dict[str, Any]:
        """
        This method sends a POST request to the RESTCONF API to retrieve platform
        information for devices configured in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the NSO query response for device platform information.

        Example:
            >>> query_helper = Query(client)
            >>> platform = query_helper.query_device_platform()
            >>> print(platform)
        """
        payload = '''
        {
            "tailf-rest-query:immediate-query": {
                "foreach": "/devices/device/platform",
                "select": [
                    {"label": "name", "expression": "../name", "result-type": ["string"]},
                    {"label": "address", "expression": "../address", "result-type": ["string"]},
                    {"label": "os", "expression": "name", "result-type": ["string"]},
                    {"label": "version", "expression": "version", "result-type": ["string"]},
                    {"label": "model", "expression": "model", "result-type": ["string"]}
                ]
            }
        }
        '''

        return self.client.query(json.loads(payload))
