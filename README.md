# cisco-nso-restconf

## Overview

This Python library provides an interface for interacting with the Cisco Network Services Orchestrator (NSO) RESTCONF API. It includes a flexible client class for direct interaction with RESTCONF _data_ resources and specific utility classes that simplify common tasks like manipulating devices.

## Features

* Raw RESTCONF API Access: Use the NSORestconfClient class to make raw GET requests to any RESTCONF ```/data``` resource.
* Utility Classes: Use pre-built helper classes such as ```Devices``` to simplify common operations like fetching all device NED ID's.

## Requirements

* NSO configuration for RESTCONF
  * To use this library, RESTCONF must be enabled in NSO. Please refer to the documentation specific to the NSO version being used to determine how to enable RESTCONF in NSO.

## Installation

You can install the package using pip:

```bash
pip install cisco-nso-restconf
```

## Usage

### Client Class

#### Methods Supported

* GET, POST, DELETE

#### Sample GET Request

You can use the NSORestconfClient class to interact with the NSO RESTCONF API ```/data``` resource by sending GET requests. This allows you to retrieve any data that the NSO system provides via RESTCONF. The following example demonstrates how to fetch all NED ID's. The client.get() method sends a GET request to the specified RESTCONF resource and returns the result as a requests ```Response```.

```python
from requests.exceptions import HTTPError, RequestException

from cisco_nso_restconf.client import NSORestconfClient

# initialize the NSORestconfClient
client = NSORestconfClient(
    scheme="http",
    address="localhost",
    port=8080,
    timeout=10,
    username="admin",
    password="admin",
)

# define resource for device NED ID's
resource = "tailf-ncs:devices/ned-ids"

try:
    # get the resource
    response = client.get(resource)

    # print the raw JSON response
    print(response.json())

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except RequestException as err:
    print(f"Requests error occurred: {err}")
except Exception as e:
    print(f"Other error occurred: {e}")

# close the session after the request is complete
client.close()
```

### Sample Life Cycle Configuration (Create/Delete VLAN Cisco IOS device)

```python
from requests.exceptions import HTTPError, RequestException

from cisco_nso_restconf.client import NSORestconfClient

# initialize the NSORestconfClient
client = NSORestconfClient(
    scheme="http",
    address="localhost",
    port=8080,
    timeout=10,
    username="admin",
    password="admin",
)

try:
    # define VLAN resource and content to create
    vlan_resource = "tailf-ncs:devices/device=ios-0/config/tailf-ned-cisco-ios:vlan"
    new_vlan_content = {"vlan-list": [{"id": 3010, "name": "Test05_3004A"}]}

    # 'dry-run' create the VLAN resource
    response = client.post(vlan_resource, new_vlan_content, params={"dry-run": "xml"})

    # print the raw JSON response from the 'dry-run'
    print(response.json())

    # create the actual VLAN resource
    response = client.post(vlan_resource, new_vlan_content)

    # if successful, get the VLAN resource we just created
    if response.status_code == 201:
        response = client.get(vlan_resource)
        print("---VLAN CREATED---")
        print(response.json())

    # delete the VLAN resource directly using the VLAN ID
    vlan_resource_delete = (
        "tailf-ncs:devices/device=ios-0/config/tailf-ned-cisco-ios:vlan/vlan-list=3010"
    )
    response = client.delete(vlan_resource_delete)

    # if successful, ensure the VLAN resource no longer has content
    if response.status_code == 204:
        print("---VLAN DELETED---")


except ValueError as val_err:
    print(f"Value error occurred: {val_err}")
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except RequestException as err:
    print(f"Other error occurred: {err}")
except Exception as e:
    print(f"Other error occurred: {e}")

# close the session after the request is complete
client.close()
```

This example demonstrates how to directly interact with the NSO RESTCONF API to create a new VLAN on a Cisco IOS device. We are showcasing how can you 'dry-run' the creation first, then actually create it, and ultimately delete it.

### Utility Classes

To make the process easier, the library also provides utility classes for specific tasks. For example, the ```Devices``` class simplifies interaction with ```tailf-ncs:devices``` RESTCONF resources.

### Sample Fetch Device NED IDs

```python
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

# initialize the Devices helper class
devices_helper = Devices(client)

# fetch device ned id's
device_ned_ids = devices_helper.get_device_ned_ids()
print(device_ned_ids)
```

#### Available Utility Classes

| Class   | Description                                            |
|---------|--------------------------------------------------------|
| Devices | Interact with the NSO ```tailf-ncs:devices``` resource |

### Closing Sessions

When using the NSORestconfClient, it’s important to close the session when you’re done to free up resources. You can do this using the close() method, as shown in the examples above.

## Contributing

We welcome contributions! Feel free to open issues or submit pull requests. For development, we recommend using Poetry to manage dependencies and packaging.

```shell
poetry install
```

## License

This project is licensed under the MIT License.

This README covers the current functionality, including how to directly use the NSORestconfClient for raw RESTCONF calls.
