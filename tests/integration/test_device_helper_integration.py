from cisco_nso_restconf.client import NSORestconfClient
from cisco_nso_restconf.devices import Devices


def test_device_get_request():
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
        # initialize the Devices helper class
        devices_helper = Devices(client)

        # fetch device ned id's
        device_ned_ids = devices_helper.get_device_ned_ids()

        # Assert that the response contains the expected key in the JSON body
        assert (
            "tailf-ncs:ned-ids" in device_ned_ids
        ), "Expected 'tailf-ncs:ned-ids' in response JSON"

    finally:
        # Ensure the session is closed, even if the test fails
        client.close()
