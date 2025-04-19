import json
from typing import Any, Dict, Optional, Union

import requests


class NSORestconfClient:
    """
    A client for interacting with the Cisco NSO RESTCONF API.

    This class provides methods to perform HTTP requests (GET, POST, DELETE)
    to the Cisco NSO RESTCONF API, allowing users to manage devices, configurations,
    and perform operations via the RESTCONF interface.

    The client manages an HTTP session for efficient reuse of connections, and
    includes parameter validation to ensure that only valid query parameters and
    values are sent with the requests.

    Attributes:
        _DATA_PATH (str): The base path for accessing RESTCONF data resources.
        _OPERATIONS_PATH (str): The base path for accessing RESTCONF operations.
        _QUERY_PATH (str): The base path for accessing RESTCONF query resources.
        _VALID_PARAMS (dict): A dictionary containing valid query parameters as keys
            and their valid values as lists. For parameters that do not require values
            (e.g., 'no-out-of-sync-check'), the value is set to `None`.

    Valid Query Parameters:
        - "dry-run": Valid values are "native", "cli", and "xml".
        - "no-out-of-sync-check": This parameter does not take a value (set to None).

    Example:
        >>> client = NSORestconfClient(
                        scheme="http",
                        address="localhost",
                        port=8080,
                        timeout=10,
                        username="admin",
                        password="admin",
                    )
        >>> response = client.get("tailf-ncs:devices/ned-ids")
        >>> print(response)

    Methods:
        get(resource, params=None):
            Sends a GET request to the specified RESTCONF resource with optional query parameters.
        post(resource, data, params=None):
            Sends a POST request to the specified RESTCONF resource with optional query parameters and data payload.
        delete(resource, params=None):
            Sends a DELETE request to the specified RESTCONF resource with optional query parameters.
        close():
            Closes the current HTTP session.
    """

    _DATA_PATH = "data"
    _OPERATIONS_PATH = "operations"
    _QUERY_PATH = "tailf/query"
    _VALID_PARAMS = {
        "dry-run": ["native", "cli", "xml"],
        "no-out-of-sync-check": [None],
    }

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

        This client interacts with two key RESTCONF resources:

        1. **Data Resource** ("/restconf/data"): Provides access to configuration and state data for standard
        CRUD operations (GET, POST, PUT, DELETE).

        2. **Operations Resource** ("/restconf/operations"): Allows access to RPC actions for non-CRUD operations,
        executed with the `action()` method via POST requests.

        Args:
            scheme (str): URL scheme (http/https). Defaults to "http".
            address (str): NSO server address. Defaults to "localhost".
            port (int): NSO server port. Defaults to 8080.
            username (Optional[str]): Authentication username. Defaults to None.
            password (Optional[str]): Authentication password. Defaults to None.
            timeout (int): Request timeout in seconds. Defaults to 30.
            disable_warning (bool): Disable SSL certificate warnings. Defaults to False.
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

    @staticmethod
    def content_to_json(content: Union[str, dict]) -> str:
        """
        Converts the given content to a JSON string.

        If the content is a dictionary, it will be serialized to a JSON string.
        If the content is already a string, it will be returned as-is.

        Args:
            content (Union[str, dict]): The content to be converted. It can either be
                                        a dictionary (which will be serialized) or a string.

        Returns:
            str: The JSON string representation of the content. If the content is already
                 a string, it will be returned unchanged.

        Example:
            >>> content_to_json({"key": "value"})
            '{"key": "value"}'
            >>> content_to_json('{"key": "value"}')
            '{"key": "value"}'
        """
        if isinstance(content, dict):
            content = json.dumps(content)

        return content

    def validate_params(self, params: Optional[Dict[str, Any]]) -> None:
        """
        Validates the query parameters provided for a RESTCONF request.

        Ensures that the `params` argument is a dictionary and that each query parameter
        is valid. If an invalid query parameter or an invalid value for a valid parameter
        is found, raises an appropriate error.

        Args:
            params (Optional[Dict[str, Any]]): A dictionary containing query parameters
                                               and their corresponding values, or None
                                               if no parameters are provided.

        Raises:
            TypeError: If `params` is not a dictionary.
            ValueError: If an invalid query parameter or value is provided.

        Example:
            >>> validate_params({"dry-run": "xml", "no-out-of-sync-check": None})
            No error raised, valid parameters.

            >>> validate_params({"invalid-param": "value"})
            Raises ValueError: Invalid query parameter: 'invalid-param'. Must be one of ['dry-run', 'no-out-of-sync-check']

            >>> validate_params({"dry-run": "invalid-value"})
            Raises ValueError: Invalid value for 'dry-run': 'invalid-value'. Must be one of ['native', 'cli', 'xml']
        """
        if params is None:
            return

        if not isinstance(params, dict):
            raise TypeError(
                f"'params' must be a dictionary, got {type(params).__name__}"
            )

        for param, value in params.items():
            if param not in self._VALID_PARAMS:
                raise ValueError(
                    f"Invalid query parameter: '{param}'. Must be one of {list(self._VALID_PARAMS.keys())}"
                )
            if (
                self._VALID_PARAMS[param] is not None
                and value not in self._VALID_PARAMS[param]
            ):
                raise ValueError(
                    f"Invalid value for '{param}': '{value}'. Must be one of {self._VALID_PARAMS[param]}"
                )

    def get(self, resource: str) -> Any:
        """
        Sends a GET request to the specified RESTCONF resource.

        Constructs the full URL using the provided resource path, sends the GET request
        to the Cisco NSO RESTCONF API, and raises an error if the response contains an
        HTTP error status. The response object is returned.

        Args:
            resource (str): The specific RESTCONF resource path to retrieve.

        Returns:
            Any: The response object from the GET request, typically containing
                 the data returned by the API in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the request returns an unsuccessful status code.

        Example:
            >>> response = client.get("tailf-ncs:devices/device")
            >>> print(response.json())
        """
        url = f"{self.base_url}/{self._DATA_PATH}/{resource}"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()

        return response

    def post(
        self,
        resource: str,
        content: Optional[Any] = None,
        params: Optional[Dict[str, Optional[str]]] = None,
    ) -> Any:
        """
        Sends a POST request to the specified RESTCONF resource with optional content and query parameters.

        Constructs the full URL using the provided resource path, validates any query parameters, converts the
        content to JSON if necessary (when provided), and sends the POST request to the Cisco NSO RESTCONF API.
        The response object is returned, and an error is raised if the response contains an HTTP error status.

        Args:
            resource (str): The specific RESTCONF resource path where the POST request is sent.
            content (Optional[Any]): The payload to send with the POST request. This can be a dictionary (converted to JSON),
                                     a raw string, or None if no content is required.
            params (Optional[Dict[str, Optional[str]]]): Optional query parameters to include in the POST request.
                                                         The keys are the parameter names, and values can be strings or None.

        Returns:
            Any: The response object from the POST request, typically containing the result of the operation or status information.

        Raises:
            TypeError: If `params` is not a dictionary (raised by `validate_params`).
            ValueError: If an invalid query parameter or value is provided (raised by `validate_params`).
            requests.exceptions.HTTPError: If the POST request returns an unsuccessful status code.

        Example:
            >>> content = {"name": "new-device", "type": "router"}
            >>> response = client.post("tailf-ncs:devices/device", content, params={"dry-run": "xml"})
            >>> print(response.json())

            >>> # POST request without content:
            >>> response = client.post("tailf-ncs:devices/device", params={"dry-run": "xml"})
            >>> print(response.status_code)
        """
        url = f"{self.base_url}/{self._DATA_PATH}/{resource}"
        self.validate_params(params)

        if content is not None:
            content = self.content_to_json(content)

        response = self.session.post(
            url,
            data=content if content is not None else None,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        return response

    def query(self, payload: Dict[str, Any]) -> Any:
        """
        Sends a query to NSO using the NSO Query API and returns the result.
        The Query API consists of a number of RPC operations to start
        queries, fetch chunks of the result from a query, restart a query,
        and stop a query

        Args:
            payload (Dict[str, Any]): The payload of the query.

        Returns:
            List[Dict]: The result of the query found in
            tailf-rest-query:query-result["result"].

        Raises:
            HTTPError: If the request to the server returns a status code that indicates a failure.
            JSONDecodeError: If the response cannot be parsed as JSON.
        
        Example:
            >>> client = NSORestconfClient(
                        scheme="http",
                        address="localhost",
                        port=8080,
                        timeout=10,
                        username="admin",
                        password="admin",
                    )
            >>> response = client.query({"tailf-rest-query:immediate-query": {"foreach": "/devices/device/platform", "select": [{"label": "name", "expression": "../name", "result-type": ["string"]}, {"label": "address", "expression": "../address", "result-type": ["string"]}, {"label": "os", "expression": "name", "result-type": ["string"]}, {"label": "version", "expression": "version", "result-type": ["string"]}, {"label": "model", "expression": "model", "result-type": ["string"]}, {"label": "serial_number", "expression": "serial-number","result-type": ["string"]}]}})
            >>> print(response)
        """
        url = f"{self.base_url}/{self._QUERY_PATH}"
        if not payload:
            raise ValueError("Payload cannot be empty")
        
        response = self.session.post(url, data=json.dumps(payload))
        response.raise_for_status()
        
        return response.json()["tailf-rest-query:query-result"].get("result")

    def delete(
        self,
        resource: str,
        content: Optional[Any] = None,
        params: Optional[Dict[str, Optional[str]]] = None,
    ) -> Any:
        """
        Sends a DELETE request to the specified RESTCONF resource with optional content and query parameters.

        This method constructs the full URL using the provided resource path, validates any query parameters,
        and sends a DELETE request to the Cisco NSO RESTCONF API. If content is provided, it is converted to JSON
        and sent as the body of the DELETE request. The response object is returned, and an error is raised if the
        response contains an HTTP error status.

        Args:
            resource (str): The specific RESTCONF resource path where the DELETE request is sent.
            content (Optional[Any]): Optional content to send with the DELETE request. This can be a dictionary
                                     (converted to JSON), a raw string, or None if no content is required.
            params (Optional[Dict[str, Optional[str]]]): Optional query parameters to include in the DELETE request.
                                                         The keys are the parameter names, and values can be strings or None.

        Returns:
            Any: The response object from the DELETE request, typically containing the result of the operation
                 or status information.

        Raises:
            TypeError: If `params` is not a dictionary (raised by `validate_params`).
            ValueError: If an invalid query parameter or value is provided (raised by `validate_params`).
            requests.exceptions.HTTPError: If the DELETE request returns an unsuccessful status code.

        Example:
            >>> # DELETE request with no content
            >>> response = client.delete("tailf-ncs:devices/device=ios-0", params={"dry-run": "xml"})
            >>> print(response.status_code)

            >>> # DELETE request with content
            >>> content = {"config": {"interface": "GigabitEthernet0/1"}}
            >>> response = client.delete("tailf-ncs:devices/device=ios-0/config", content=content, params={"dry-run": "cli"})
            >>> print(response.json())
        """
        url = f"{self.base_url}/{self._DATA_PATH}/{resource}"
        self.validate_params(params)

        if content is not None:
            content = self.content_to_json(content)

        response = self.session.delete(
            url,
            data=content if content is not None else None,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        return response

    def close(self) -> None:
        """
        Closes the current HTTP session.

        This method terminates the HTTP session used for making requests to the
        Cisco NSO RESTCONF API. It is important to call this method when the
        client is no longer needed to free up resources and properly close
        connections.

        Example:
            >>> client = NSORestconfClient(
                        scheme="http",
                        address="localhost",
                        port=8080,
                        timeout=10,
                        username="admin",
                        password="admin",
                    )
            >>> # Perform some operations with the client...
            >>> client.close()  # Closes the session when done
        """
        self.session.close()
