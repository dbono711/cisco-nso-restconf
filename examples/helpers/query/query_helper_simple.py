from requests.exceptions import HTTPError, RequestException
import json
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

from cisco_nso_restconf.client import NSORestconfClient
from cisco_nso_restconf.query import Query

# initialize the NSORestconfClient
client = NSORestconfClient(
    scheme="http",
    address="localhost",
    port=8080,
    timeout=10,
    username="admin",
    password="admin",
)

# initialize the Query helper class
query_helper = Query(client)

# create a Rich console for pretty printing
console = Console()

try:
    device_platform = query_helper.query_device_platform()
    print(device_platform)

    devices = {}
    for device_entry in device_platform:
        device_info = {}
        device_name = None
    
        # Extract all label-value pairs for this device
        for item in device_entry['select']:
            label = item['label']
            value = item['value']
        
            # Store the device name to use as the key
            if label == 'name':
                device_name = value
            else:
                # Convert label to snake_case if needed (already done in your data)
                device_info[label] = value
    
        # Add the device to our dictionary if we found a name
        if device_name:
            devices[device_name] = device_info
    
    console.print(Panel.fit(
        JSON(json.dumps(devices)),
        title="[bold blue]DEVICE PLATFORM INFO[/bold blue]",
        border_style="blue"
    ))
except ValueError as val_err:
    console.print(f"[bold red]Value error occurred:[/bold red] {val_err}")
except HTTPError as http_err:
    console.print(f"[bold red]HTTP error occurred:[/bold red] {http_err}")
except RequestException as err:
    console.print(f"[bold red]Other error occurred:[/bold red] {err}")
except Exception as e:
    console.print(f"[bold red]Other error occurred:[/bold red] {e}")
finally:
    # always close the client session
    client.close()
