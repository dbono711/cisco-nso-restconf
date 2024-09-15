from cisco_nso_restconf.client import NSORestconfClient


def test_get_request(mocker):
    # Mock the requests.Session object
    mock_session = mocker.patch("requests.Session")

    # Mock the GET response
    mock_response = mock_session.return_value.get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"tailf-ncs:ned-ids": {}}

    # Create the client (this will use the mocked session)
    client = NSORestconfClient(
        scheme="http",
        address="localhost",
        port=8080,
        timeout=10,
        username="admin",
        password="admin",
    )

    # Perform the GET request
    response = client.get("tailf-ncs:devices/ned-ids")

    # Assert that the response JSON matches the expected dictionary
    assert response.json() == {"tailf-ncs:ned-ids": {}}

    # Ensure the session is closed
    client.close()
