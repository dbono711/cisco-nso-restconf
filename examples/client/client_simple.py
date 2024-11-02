"""
You can use the NSORestconfClient class to interact with the NSO RESTCONF API
```/data``` resource by sending GET requests. This allows you to retrieve any
data that the NSO system provides via RESTCONF. The following example demonstrates
how to fetch all NED ID's. The client.get() method sends a GET request to the
specified RESTCONF resource and returns the result as a requests ```Response```.
"""

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

# define the resource
resource = "tailf-ncs:devices/ned-ids"

try:
    # get the resource
    response = client.get(resource)

    # print the JSON response
    print(response.json())

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except RequestException as err:
    print(f"Requests error occurred: {err}")
except Exception as e:
    print(f"Other error occurred: {e}")
finally:
    # always close the client session
    client.close()
