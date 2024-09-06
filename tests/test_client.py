from cisco_nso_restconf.client import NSORestconfClient


def test_get_request_real():
    client = NSORestconfClient(
        scheme="http",
        address="localhost",
        port=8080,
        timeout=10,
        username="admin",
        password="admin",
    )

    response = client.get("tailf-ncs:devices/ned-ids")
    assert "tailf-ncs:ned-ids" in response
    client.close()


def test_get_request_mock(mocker):
    mock_session = mocker.patch("requests.Session")
    mock_response = mock_session.return_value.get.return_value
    mock_response.json.return_value = {"tailf-ncs:ned-ids": {}}

    client = NSORestconfClient(
        scheme="http",
        address="localhost",
        port=8080,
        timeout=10,
        username="admin",
        password="admin",
    )

    response = client.get("tailf-ncs:devices/ned-ids")
    assert response == {"tailf-ncs:ned-ids": {}}
    client.close()
