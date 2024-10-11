from typing import Any, Dict

from .client import NSORestconfClient


class Devices:
    """
    A helper class for interacting with the Cisco NSO 'tailf-ncs:devices' resource via RESTCONF.

    This class provides methods to interact with device-related resources in the Cisco NSO system,
    using the `NSORestconfClient` to perform underlying REST operations.
    """

    def __init__(self, client: NSORestconfClient):
        """
        Initializes the Devices helper class.

        Args:
            client (NSORestconfClient): An instance of NSORestconfClient used to send RESTCONF requests.
        """
        self.client = client

    def get_device_ned_ids(self) -> Dict[str, Any]:
        """
        This method sends a GET request to the RESTCONF API to retrieve the available
        Network Element Driver (NED) IDs in Cisco NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the NED IDs.

        Example:
            >>> devices_helper = Devices(client)
            >>> ned_ids = devices_helper.get_device_ned_ids()
            >>> print(ned_ids)
        """
        resource = "tailf-ncs:devices/ned-ids"
        return self.client.get(resource).json()

    def get_device_groups(self) -> Dict[str, Any]:
        """
        This method sends a GET request to the RESTCONF API to retrieve configured
        device groups in Cisco NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the device groups.

        Example:
            >>> devices_helper = Devices(client)
            >>> ned_ids = devices_helper.get_device_groups()
            >>> print(ned_ids)
        """
        resource = "tailf-ncs:devices/device-group"
        return self.client.get(resource).json()

    def get_device_platform(self, device_name: str) -> Dict[str, Any]:
        """
        This method sends a GET request to the RESTCONF API to retrieve platform
        information for a device configured in NSO.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the device platform information.

        Example:
            >>> devices_helper = Devices(client)
            >>> device1_platform = devices_helper.get_device_platform("device1")
            >>> print(device1_platform)
        """
        resource = f"tailf-ncs:devices/device={device_name}/platform"
        return self.client.get(resource).json()
