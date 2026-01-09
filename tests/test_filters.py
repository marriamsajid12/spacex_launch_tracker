from datetime import datetime
from spacex_tracker.launch import Launch, LaunchService


def test_filter_success():
    service = LaunchService()

    launches = [
        Launch("A", datetime(2020, 1, 1), True, "Falcon 9", "X"),
        Launch("B", datetime(2020, 1, 2), False, "Falcon 9", "X"),
    ]

    result = service.filter_launches(launches, success=True)
    assert len(result) == 1
