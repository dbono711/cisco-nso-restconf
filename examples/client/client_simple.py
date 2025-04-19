"""
You can use the NSORestconfClient class to interact with the NSO RESTCONF API
```/data``` resource by sending GET requests. This allows you to retrieve any
data that the NSO system provides via RESTCONF. The following example demonstrates
how to fetch all NED ID's. The client.get() method sends a GET request to the
specified RESTCONF resource and returns the result as a requests ```Response```.
"""

from requests.exceptions import HTTPError, RequestException

from cisco_nso_restconf.client import NSORestconfClient
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
import json

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

# create a Rich console for pretty printing
console = Console()

try:
    # get the resource
    response = client.get(resource)

    # print the JSON response
    console.print(Panel.fit(
        JSON(json.dumps(response.json())),
        title="[bold blue]DEVICE PLATFORM INFO[/bold blue]",
        border_style="blue"
    ))

except HTTPError as http_err:
    console.print(f"[bold red]HTTP error occurred:[/bold red] {http_err}")
except RequestException as err:
    console.print(f"[bold red]Requests error occurred:[/bold red] {err}")
except Exception as e:
    console.print(f"[bold red]Other error occurred:[/bold red] {e}")
finally:
    # always close the client session
    client.close()
