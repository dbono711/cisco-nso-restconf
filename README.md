# cisco-nso-restconf

## Overview

This Python library provides an interface for interacting with the Cisco NSO RESTCONF API. It includes a flexible client class for direct interaction with RESTCONF _data_ resources.

## Features

* Raw RESTCONF API Access: Use the NSORestconfClient class to make raw GET requests to any RESTCONF endpoint.

## Installation

You can install the package using pip:

```bash
pip install cisco-nso-restconf
```

## Usage

### Client Class

You can use the NSORestconfClient class to directly interact with the RESTCONF API by sending raw requests. This allows you to retrieve any data that the NSO system provides via RESTCONF.

```python
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

# send a raw GET request to a RESTCONF resource
resource = "tailf-ncs:devices/ned-ids"
response = client.get(resource)

# print the raw JSON response
print(response)

# close the session after the request is complete
client.close()
```

This example demonstrates how to directly interact with the NSO RESTCONF API to fetch all NED ID's. The client.get() method sends a GET request to the specified RESTCONF resource and returns the result as a Python dictionary.

#### Methods Supported

* GET

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
