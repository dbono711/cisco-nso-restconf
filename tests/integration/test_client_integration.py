from cisco_nso_restconf.client import NSORestconfClient


def test_get_request():
    client = NSORestconfClient(
        scheme="http",
        address="localhost",
        port=8080,
        timeout=10,
        username="admin",
        password="admin",
    )

    try:
        # Perform the GET request
        response = client.get("tailf-ncs:devices/ned-ids")

        # Assert that the response status code is 200 (successful)
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"

        # Assert that the response contains the expected key in the JSON body
        assert (
            "tailf-ncs:ned-ids" in response.json()
        ), "Expected 'tailf-ncs:ned-ids' in response JSON"

    finally:
        # Ensure the session is closed, even if the test fails
        client.close()


def test_post_dry_run_request():
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
        response = client.post(
            vlan_resource, new_vlan_content, params={"dry-run": "xml"}
        )

        # Assert that the response status code is 201 (created)
        assert (
            response.status_code == 201
        ), f"Unexpected status code: {response.status_code}"

        # Assert that the response contains the expected key in the JSON body
        assert (
            "dry-run-result" in response.json()
        ), "Expected 'dry-run-result' in response JSON"

    finally:
        # Ensure the session is closed, even if the test fails
        client.close()
