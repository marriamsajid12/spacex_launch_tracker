from datetime import datetime
from typing import List, Dict, Any, Optional
from spacex_tracker.spacex_api import SpaceXAPI
from spacex_tracker.cache import load_cache, save_cache
from dataclasses import dataclass

@dataclass
class Launch:
    name: str
    date_utc: datetime
    success: Optional[bool]
    rocket: str
    launchpad: str

class LaunchService:
    def __init__(self):
        self.api = SpaceXAPI()
        self.rocket_map: Dict[str, str] = {}
        self.launchpad_map: Dict[str, str] = {}
        self._load_mappings()


    def _load_mappings(self) -> None:
        """Fetch rockets and launchpads, cache them, create id to name maps."""

        # Rockets
        try:
            cached_rockets = load_cache("rockets")
            if cached_rockets:
                rockets = cached_rockets
            else:
                rockets = self.api.fetch("rockets")
                save_cache("rockets", rockets)
            self.rocket_map = {r["id"]: r["name"] for r in rockets}
        except Exception as e:
            print(f"Warning: Failed to fetch rockets: {e}")

        # Launchpads
        try:
            cached_launchpads = load_cache("launchpads")
            if cached_launchpads:
                launchpads = cached_launchpads
            else:
                launchpads = self.api.fetch("launchpads")
                save_cache("launchpads", launchpads)
            self.launchpad_map = {l["id"]: l["name"] for l in launchpads}
        except Exception as e:
            print(f"Warning: Failed to fetch launchpads: {e}")


    def get_launches(self) -> List[Launch]:
        """
        Fetch launches from cache or API.
        Returns a list of Launch objects with human-readable rocket/launchpad names.
        """
        # Loading from cache
        try:
            cached = load_cache("launches")
            if cached:
                return self._parse_launches(cached)
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")

        # Fetch from API
        try:
            raw_launches = self.api.fetch("launches")
        except Exception as e:
            print(f"Error fetching launches from API: {e}")
            return []

        # Save to cache
        try:
            save_cache("launches", raw_launches)
        except Exception as e:
            print(f"Warning: Failed to save cache: {e}")

        # Parse raw data
        try:
            return self._parse_launches(raw_launches)
        except Exception as e:
            print(f"Error parsing launches data: {e}")
            return []

    def _parse_launches(self, data: List[Dict[str, Any]]) -> List[Launch]:
        """
        Convert raw API or cache data into Launch objects.
        Replaces rocket and launchpad IDs with human-readable names.
        """
        launches: List[Launch] = []
        for i, item in enumerate(data):
            try:
                rocket_id = item.get("rocket", "")
                launchpad_id = item.get("launchpad", "")
                rocket_name = self.rocket_map.get(rocket_id, rocket_id or "Unknown")
                launchpad_name = self.launchpad_map.get(launchpad_id, launchpad_id or "Unknown")

                date_str = item.get("date_utc")
                if not date_str:
                    raise ValueError("Missing date_utc")

                launches.append(
                    Launch(
                        name=item.get("name", "Unknown"),
                        date_utc=datetime.fromisoformat(date_str.replace("Z", "")),
                        success=item.get("success", False),
                        rocket=rocket_name,
                        launchpad=launchpad_name,
                    )
                )
            except Exception as e:
                print(f"Unexpected error parsing launch {i}: {e}, skipping.")
        return launches


    def filter_launches(
        self,
        launches: List[Launch],
        name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        rocket: Optional[str] = None,
        success: Optional[bool] = None,
        launchpad: Optional[str] = None,
    ) -> List[Launch]:

        result = launches

        if start_date:
            result = [
                l for l in result
                if isinstance(l.date_utc, datetime) and l.date_utc >= start_date
            ]

        if end_date:
            result = [
                l for l in result
                if isinstance(l.date_utc, datetime) and l.date_utc <= end_date
            ]

        if name:
            name = name.lower().strip()
            result = [
                l for l in result
                if l.name.lower().strip() == name
            ]

        if rocket:
            rocket = rocket.lower().strip()
            result = [
                l for l in result
                if l.rocket.lower().strip() == rocket
            ]

        if success is not None:
            result = [
                l for l in result
                if l.success is success
            ]

        if launchpad:
            launchpad = launchpad.lower().strip()
            result = [
                l for l in result
                if l.launchpad.lower().strip() == launchpad
            ]

        return result

