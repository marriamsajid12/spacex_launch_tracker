from typing import List, Dict, Any
import requests

BASE_URL = "https://api.spacexdata.com/v4"


class SpaceXError(Exception):
    """Custom exception for SpaceX API errors"""
    pass


class SpaceXAPI:
    def fetch(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Fetch data from SpaceX API.

        Args: 
            endpoint (str): API endpoint to fetch data from (e.g., "launches")

        Returns: 
            List[Dict[str, Any]]: JSON response as a list of dictionaries

        """
        url = f"{BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad status codes
        except requests.exceptions.RequestException as e:
            raise SpaceXError(f"Error fetching '{endpoint}': {e}")

        try:
            data = response.json()
            if not isinstance(data, list):
                raise SpaceXError(f"Unexpected response format for '{endpoint}': expected list")
            return data
        except Exception as e:
            raise SpaceXError(f"Unexpected error parsing '{endpoint}' response: {e}")
