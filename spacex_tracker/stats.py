from collections import defaultdict
from typing import Dict, List
from spacex_tracker.launch import Launch


def success_rate_by_rocket(launches: List[Launch]) -> Dict[str, float]:
    """
    Calculate the success rate of launches for each rocket.
    """
    stats = defaultdict(lambda: {"success": 0, "total": 0})

    for i, launch in enumerate(launches):
        try:
            if not launch.rocket:
                raise ValueError("Rocket field missing")
            stats[launch.rocket]["total"] += 1
            if launch.success:
                stats[launch.rocket]["success"] += 1
        except Exception as e:
            print(f"Warning: Skipping launch {i} in success_rate_by_rocket: {e}")

    # Calculate rate
    result = {}
    for rocket, data in stats.items():
        try:
            result[rocket] = data["success"] / data["total"]
        except Exception as e:
            print(f"Warning: Could not calculate success rate for {rocket}: {e}")
            result[rocket] = 0.0

    return result


def launches_per_site(launches: List[Launch]) -> Dict[str, int]:
    """
    Count total launches per launch site.
    """
    counts = defaultdict(int)
    for i, launch in enumerate(launches):
        try:
            if not launch.launchpad:
                raise ValueError("Launchpad field missing")
            counts[launch.launchpad] += 1
        except Exception as e:
            print(f"Warning: Skipping launch {i} in launches_per_site: {e}")
    return dict(counts)


def launch_frequency(launches: List[Launch]) -> Dict[str, int]:
    """
    Count launches per month in format YYYY-MM.
    """
    freq = defaultdict(int)
    for i, launch in enumerate(launches):
        try:
            if not launch.date_utc:
                raise ValueError("date field missing")
            key = launch.date_utc.strftime("%Y-%m")
            freq[key] += 1
        except Exception as e:
            print(f"Warning: Skipping launch {i} in launch_frequency: {e}")
    return dict(freq)


def launch_frequency_monthly(launches: List[Launch]) -> Dict[str, int]:
    """
    Count launches per month in format YYYY-MM.
    """
    freq = defaultdict(int)
    for i, launch in enumerate(launches):
        try:
            if not launch.date_utc:
                raise ValueError("date field missing")
            key = launch.date_utc.strftime("%Y-%m")
            freq[key] += 1
        except Exception as e:
            print(f"Warning: Skipping launch {i} in launch_frequency_monthly: {e}")
    return dict(freq)


def launch_frequency_yearly(launches: List[Launch]) -> Dict[str, int]:
    """
    Count launches per year in format YYYY.
    """
    freq = defaultdict(int)
    for i, launch in enumerate(launches):
        try:
            if not launch.date_utc:
                raise ValueError("date field missing")
            key = launch.date_utc.strftime("%Y")
            freq[key] += 1
        except Exception as e:
            print(f"Warning: Skipping launch {i} in launch_frequency_yearly: {e}")
    return dict(freq)

