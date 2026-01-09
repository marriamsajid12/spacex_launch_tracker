from unittest.mock import patch
from spacex_tracker.spacex_api import SpaceXAPI


@patch("requests.get")
def test_api_fetch(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"name": "Test Launch"}]

    api = SpaceXAPI()
    data = api.fetch("launches")

    assert data[0]["name"] == "Test Launch"
