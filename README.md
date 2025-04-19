# cisco-nso-restconf

## Overview

This Python library provides an interface for interacting with the Cisco Network Services Orchestrator (NSO) RESTCONF API.

## Features

* **RESTCONF API Access:** Use the [NSORestconfClient](cisco_nso_restconf/client.py) class to make raw GET, POST, & DELETE requests to any RESTCONF ```/data``` resource.
* **Utility Classes:** Use pre-built helper classes, such as the [Devices](cisco_nso_restconf/devices.py) class, or [Query](cisco_nso_restconf/query.py) class, to simplify common operations, like fetching all device NED ID's.

## Requirements

* NSO RESTCONF Configuration
  * To use this library, RESTCONF must be enabled in NSO. Please refer to the documentation specific to the NSO version being used to determine how to enable RESTCONF in NSO.

## Installation

You can install the library using pip:

```bash
pip install cisco-nso-restconf
```

## Client Class

Use the [NSORestconfClient](cisco_nso_restconf/client.py) class to interact with the NSO RESTCONF API ```/data``` resource

### Methods Supported

* GET, POST, DELETE

## Utility Classes

To make the process easier, the library also provides utility classes for specific tasks. For example, the [Devices](cisco_nso_restconf/devices.py) class simplifies interaction with ```tailf-ncs:devices``` RESTCONF resources.

### Available Utility Classes

| Class   | Description                                            |
|---------|--------------------------------------------------------|
| Devices | Interact with the NSO ```tailf-ncs:devices``` resource |
| Query   | Interact with the NSO ```tailf-ncs:query``` resource   |

### Closing Sessions

When using the NSORestconfClient, it’s important to close the session when you’re done to free up resources. You can do this using the close() method, as shown in the examples above.

## Examples

There are a number of [examples](examples) provided for utilizing the Client classes and various Helper classes, such as the ```Devices``` class. The examples are intended to showcase basic use cases/workflows for achieving a specific function in NSO, such as retrieving NED ID's, device groups, life cycle of a VLAN resource, life cycle of a service, and so on.

### Running Examples

To run the examples, you'll need to install the development dependencies which include the `rich` library for enhanced terminal output. Use [UV](https://docs.astral.sh/uv/) to install these dependencies:

```shell
uv sync
```

This will install all required dependencies, including those needed for the examples. Without installing the development dependencies, the examples that use the `rich` library for output formatting will not work.

## Contributing

We welcome contributions! Feel free to open issues or submit pull requests. For development, we recommend using [UV](https://docs.astral.sh/uv/) to manage dependencies and packaging.

```shell
uv sync
```

## License

This project is licensed under the MIT License.
