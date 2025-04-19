from cisco_nso_restconf.client import NSORestconfClient
from cisco_nso_restconf.query import Query


def test_device_query_request():
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
        # initialize the Query helper class
        query_helper = Query(client)

        # fetch device platform information
        device_platform = query_helper.query_device_platform()

        # Test that the response is a list
        assert isinstance(device_platform, list), "Expected response to be a list"
        
        # Test that the list is not empty (assuming there are devices in NSO)
        assert len(device_platform) > 0, "Expected at least one device in the response"
        
        # Test the structure of the first device entry
        first_device = device_platform[0]
        assert 'select' in first_device, "Expected 'select' key in device entry"
        assert isinstance(first_device['select'], list), "Expected 'select' value to be a list"
        
        # Test that the select list contains label-value pairs
        select_items = first_device['select']
        assert len(select_items) > 0, "Expected at least one item in 'select' list"
        
        # Test the structure of a select item
        first_item = select_items[0]
        assert 'label' in first_item, "Expected 'label' key in select item"
        assert 'value' in first_item, "Expected 'value' key in select item"
        
        # Test that required fields are present in the response
        required_labels = {'name', 'address', 'os', 'version', 'model'}
        found_labels = {item['label'] for item in select_items}
        assert required_labels.issubset(found_labels), f"Missing required labels. Expected {required_labels}, found {found_labels}"

    finally:
        # Ensure the session is closed, even if the test fails
        client.close()
