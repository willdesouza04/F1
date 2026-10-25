"""OpenF1 API client."""

import requests

from .exceptions import APIError, NetworkError, NotFoundError


class OpenF1Client:
    """Synchronous HTTP client for the OpenF1 API."""

    def __init__(self, base_url: str = "https://api.openf1.org/v1", timeout: int = 30):
        """Initialize the OpenF1 client.

        Args:
            base_url: Base URL for the OpenF1 API.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout

    def _fetch(self, endpoint: str, params: dict = None) -> list[dict]:
        """Fetch data from an endpoint.

        Args:
            endpoint: API endpoint (e.g., "/meetings").
            params: Query parameters.

        Returns:
            List of dictionaries with the API response.

        Raises:
            NetworkError: If there is a connection/timeout error.
            NotFoundError: If the resource is not found (404).
            APIError: If the API returns an error (4xx/5xx).
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params or {}, timeout=self.timeout)
        except (requests.ConnectionError, requests.Timeout) as e:
            raise NetworkError(f"Connection failed: {e}") from e

        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.status_code} at {url}")

        if response.status_code >= 400:
            raise APIError(f"API error: {response.status_code} at {url}")

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise APIError(f"Failed to parse JSON response: {e}") from e

    def get_meetings(self, year: int = None, **filters) -> list[dict]:
        """Get Formula 1 meetings.

        Args:
            year: Filter by year (e.g., 2024).
            **filters: Additional query parameters.

        Returns:
            List of meeting dictionaries.
        """
        params = {}
        if year is not None:
            params["year"] = year
        params.update(filters)
        return self._fetch("/meetings", params)

    def get_sessions(self, year: int = None, **filters) -> list[dict]:
        """Get Formula 1 sessions.

        Args:
            year: Filter by year.
            **filters: Additional query parameters.

        Returns:
            List of session dictionaries.
        """
        params = {}
        if year is not None:
            params["year"] = year
        params.update(filters)
        return self._fetch("/sessions", params)

    def get_drivers(self, session_key: int, **filters) -> list[dict]:
        """Get drivers for a session.

        Args:
            session_key: Session key (required).
            **filters: Additional query parameters.

        Returns:
            List of driver dictionaries.
        """
        params = {"session_key": session_key}
        params.update(filters)
        return self._fetch("/drivers", params)

    def get_laps(self, session_key: int, **filters) -> list[dict]:
        """Get lap data for a session.

        Args:
            session_key: Session key (required).
            **filters: Additional query parameters (e.g., driver_number).

        Returns:
            List of lap dictionaries.
        """
        params = {"session_key": session_key}
        params.update(filters)
        return self._fetch("/laps", params)

    def get_car_data(self, session_key: int, **filters) -> list[dict]:
        """Get car telemetry for a session.

        Args:
            session_key: Session key (required).
            **filters: Additional query parameters.

        Returns:
            List of car data dictionaries.
        """
        params = {"session_key": session_key}
        params.update(filters)
        return self._fetch("/car_data", params)
