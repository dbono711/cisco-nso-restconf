"""
This example demonstrates how to directly interact with the NSO RESTCONF API
to create a new VLAN on a Cisco IOS device. We are showcasing how can you
'dry-run' the creation first, then actually create it, and ultimately delete it.
"""

from requests.exceptions import HTTPError, RequestException

from cisco_nso_restconf.client import NSORestconfClient


def create_vlan(client, resource, vlan_data, dry_run=False):
    params = {"dry-run": "xml"} if dry_run else {}
    response = client.post(resource, vlan_data, params=params)

    if response.status_code == 201:
        return response
    else:
        raise HTTPError(f"Unexpected status code {response.status_code}")


def delete_vlan(client, resource):
    response = client.delete(resource)
    if response.status_code != 204:
        raise HTTPError(f"Failed to delete VLAN. Status code: {response.status_code}")
    return True


def main():
    # initialize the NSORestconfClient
    client = NSORestconfClient(
        scheme="http",
        address="localhost",
        port=8080,
        timeout=10,
        username="admin",
        password="admin",
    )

    vlan_resource = "tailf-ncs:devices/device=ios-0/config/tailf-ned-cisco-ios:vlan"
    new_vlan = {"vlan-list": [{"id": 3010, "name": "Test05_3004A"}]}
    vlan_resource_delete = (
        "tailf-ncs:devices/device=ios-0/config/tailf-ned-cisco-ios:vlan/vlan-list=3010"
    )

    try:
        # Perform a dry-run VLAN creation
        print("---DRY-RUN---")
        dry_run_result = create_vlan(client, vlan_resource, new_vlan, dry_run=True)
        print(dry_run_result.json())
        print()

        # Create the VLAN resource
        print("---VLAN CREATION---")
        create_vlan(client, vlan_resource, new_vlan)
        print("VLAN created successfully.")
        print()

        # Fetch and display the VLAN resource after creation
        print("---FETCHING CREATED VLAN---")
        vlan_response = client.get(vlan_resource)
        print(vlan_response.json())
        print()

        # Delete the VLAN resource
        print("---DELETING VLAN---")
        if delete_vlan(client, vlan_resource_delete):
            print("VLAN deleted successfully.")

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        # always close the client session
        client.close()


if __name__ == "__main__":
    main()
