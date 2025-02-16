from requests.exceptions import HTTPError, RequestException
import json
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

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

# create a Rich console for pretty printing
console = Console()

try:
    device_ned_ids = devices_helper.get_device_ned_ids()
    console.print(Panel.fit(
        JSON(json.dumps(device_ned_ids)),
        title="[bold blue]DEVICE NED IDS[/bold blue]",
        border_style="blue"
    ))

    device_groups = devices_helper.get_device_groups()
    console.print(Panel.fit(
        JSON(json.dumps(device_groups)),
        title="[bold green]DEVICE GROUPS[/bold green]",
        border_style="green"
    ))

    p_central_platform = devices_helper.get_device_platform("p_central")
    console.print(Panel.fit(
        JSON(json.dumps(p_central_platform)),
        title="[bold yellow]DEVICE PLATFORM: p_central[/bold yellow]",
        border_style="yellow"
    ))

    p_central_config = devices_helper.get_device_config("p_central")
    console.print(Panel.fit(
        JSON(json.dumps(p_central_config)),
        title="[bold yellow]DEVICE CONFIG: p_central[/bold yellow]",
        border_style="yellow"
    ))

    p_central_state = devices_helper.get_device_state("p_central")
    console.print(Panel.fit(
        JSON(json.dumps(p_central_state)),
        title="[bold yellow]DEVICE STATE: p_central[/bold yellow]",
        border_style="yellow"
    ))

    iosxr_0_check_sync = devices_helper.check_sync("iosxr-0")
    console.print(Panel.fit(
        JSON(json.dumps(iosxr_0_check_sync)),
        title="[bold yellow]DEVICE SYNC STATUS: iosxr-0[/bold yellow]",
        border_style="yellow"
    ))

    iosxr_0_sync_from = devices_helper.sync_from_device("iosxr-0")
    console.print(Panel.fit(
        JSON(json.dumps(iosxr_0_sync_from)),
        title="[bold yellow]DEVICE SYNC-FROM STATUS: iosxr-0[/bold yellow]",
        border_style="yellow"
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
