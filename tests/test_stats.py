from datetime import datetime
from spacex_tracker.launch import Launch
from spacex_tracker.stats import success_rate_by_rocket


def test_success_rate():
    launches = [
        Launch("A", datetime.now(), True, "Falcon 9", "X"),
        Launch("B", datetime.now(), False, "Falcon 9", "X"),
    ]

    rates = success_rate_by_rocket(launches)
    assert rates["Falcon 9"] == 0.5
