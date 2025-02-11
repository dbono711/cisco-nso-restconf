from requests.exceptions import HTTPError, RequestException

from cisco_nso_restconf.client import NSORestconfClient
from cisco_nso_restconf.devices import Devices

# initialize the NSORestconfClient
client = NSORestconfClient(
    scheme="http",
    address="localhost",
    port=8080,
    timeout=10,
    username="admin",
    password="admin",
)

# initialize the Devices class
devices_helper = Devices(client)

# fetch device ned id's
try:
    device_ned_ids = devices_helper.get_device_ned_ids()
    print("---DEVICE NED IDS---")
    print(device_ned_ids)
    print()

    device_groups = devices_helper.get_device_groups()
    print("---DEVICE GROUPS---")
    print(device_groups)
    print()

    p_central_platform = devices_helper.get_device_platform("p_central")
    print("---DEVICE PLATFORM---")
    print(p_central_platform)
    print()

except ValueError as val_err:
    print(f"Value error occurred: {val_err}")
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except RequestException as err:
    print(f"Other error occurred: {err}")
except Exception as e:
    print(f"Other error occurred: {e}")
finally:
    # always close the client session
    client.close()
