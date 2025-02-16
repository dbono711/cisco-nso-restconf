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
    
    def get_device_config(self, device_name: str) -> Dict[str, Any]:
        """
        Retrieves the running configuration of a specific device from NSO.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the device's running configuration.

        Example:
            >>> devices_helper = Devices(client)
            >>> config = devices_helper.get_device_config("device1")
            >>> print(config)
        """
        resource = f"tailf-ncs:devices/device={device_name}/config"
        return self.client.get(resource).json()

    def get_device_state(self, device_name: str) -> Dict[str, Any]:
        """
        Retrieves the operational state of a device including connection status.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the device's state information.

        Example:
            >>> devices_helper = Devices(client)
            >>> state = devices_helper.get_device_state("device1")
            >>> print(state)
        """
        resource = f"tailf-ncs:devices/device={device_name}/state"
        return self.client.get(resource).json()

    def check_sync(self, device_name: str) -> Dict[str, Any]:
        """
        Checks if the device configuration in NSO is in sync with the actual device.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the sync status information.

        Example:
            >>> devices_helper = Devices(client)
            >>> status = devices_helper.check_sync("device1")
            >>> print(status)
        """
        resource = f"tailf-ncs:devices/device={device_name}/check-sync"
        return self.client.post(resource).json()
    
    def sync_from_device(self, device_name: str) -> Dict[str, Any]:
        """
        Triggers a sync-from operation to synchronize NSO's configuration with the device.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the sync operation result.

        Example:
            >>> devices_helper = Devices(client)
            >>> result = devices_helper.sync_from_device("device1")
            >>> print(result)
        """
        resource = f"tailf-ncs:devices/device={device_name}/sync-from"
        return self.client.post(resource).json()

    def connect_device(self, device_name: str) -> Dict[str, Any]:
        """
        Initiates a connection to the device.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the connection operation result.

        Example:
            >>> devices_helper = Devices(client)
            >>> result = devices_helper.connect_device("device1")
            >>> print(result)
        """
        resource = f"tailf-ncs:devices/device={device_name}/connect"
        return self.client.post(resource).json()

    def disconnect_device(self, device_name: str) -> Dict[str, Any]:
        """
        Disconnects from the device.

        Args:
            device_name (str): The hostname of the device in NSO.

        Returns:
            Dict[str, Any]: A dictionary containing the disconnect operation result.

        Example:
            >>> devices_helper = Devices(client)
            >>> result = devices_helper.disconnect_device("device1")
            >>> print(result)
        """
        resource = f"tailf-ncs:devices/device={device_name}/disconnect"
        return self.client.post(resource).json()