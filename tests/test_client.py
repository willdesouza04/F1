"""Tests for the OpenF1Client."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from f1.client import OpenF1Client
from f1.exceptions import APIError, NetworkError, NotFoundError


class TestOpenF1ClientInit:
    """Tests for OpenF1Client initialization."""

    def test_init_with_defaults(self):
        """Test client initialization with default parameters."""
        client = OpenF1Client()
        assert client.base_url == "https://api.openf1.org/v1"
        assert client.timeout == 30

    def test_init_with_custom_url(self):
        """Test client initialization with custom base URL."""
        custom_url = "https://custom.api.com"
        client = OpenF1Client(base_url=custom_url)
        assert client.base_url == custom_url

    def test_init_with_custom_timeout(self):
        """Test client initialization with custom timeout."""
        client = OpenF1Client(timeout=60)
        assert client.timeout == 60


class TestOpenF1ClientFetch:
    """Tests for the _fetch method."""

    def test_fetch_success(self, api_client, sample_meetings):
        """Test successful fetch."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_meetings
            mock_get.return_value = mock_response

            result = api_client._fetch("/meetings")
            assert result == sample_meetings
            mock_get.assert_called_once()

    def test_fetch_connection_error(self, api_client):
        """Test fetch with connection error."""
        with patch("f1.client.requests.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError("Connection failed")

            with pytest.raises(NetworkError):
                api_client._fetch("/meetings")

    def test_fetch_timeout_error(self, api_client):
        """Test fetch with timeout error."""
        with patch("f1.client.requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout("Request timeout")

            with pytest.raises(NetworkError):
                api_client._fetch("/meetings")

    def test_fetch_not_found(self, api_client):
        """Test fetch with 404 error."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            with pytest.raises(NotFoundError):
                api_client._fetch("/invalid")

    def test_fetch_api_error(self, api_client):
        """Test fetch with 5xx error."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response

            with pytest.raises(APIError):
                api_client._fetch("/meetings")

    def test_fetch_json_decode_error(self, api_client):
        """Test fetch with invalid JSON response."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
                "Invalid JSON", "", 0
            )
            mock_get.return_value = mock_response

            with pytest.raises(APIError):
                api_client._fetch("/meetings")


class TestOpenF1ClientMeetings:
    """Tests for the get_meetings method."""

    def test_get_meetings(self, api_client, sample_meetings):
        """Test getting meetings."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_meetings
            mock_get.return_value = mock_response

            result = api_client.get_meetings()
            assert result == sample_meetings

    def test_get_meetings_with_year(self, api_client, sample_meetings):
        """Test getting meetings filtered by year."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_meetings
            mock_get.return_value = mock_response

            result = api_client.get_meetings(year=2024)
            assert result == sample_meetings

            # Verify year was passed as parameter
            call_args = mock_get.call_args
            assert call_args[1]["params"]["year"] == 2024


class TestOpenF1ClientSessions:
    """Tests for the get_sessions method."""

    def test_get_sessions(self, api_client):
        """Test getting sessions."""
        sample_sessions = [{"session_key": 9158, "session_name": "Practice 1"}]
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_sessions
            mock_get.return_value = mock_response

            result = api_client.get_sessions()
            assert result == sample_sessions


class TestOpenF1ClientDrivers:
    """Tests for the get_drivers method."""

    def test_get_drivers(self, api_client, sample_drivers):
        """Test getting drivers."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_drivers
            mock_get.return_value = mock_response

            result = api_client.get_drivers(session_key=9158)
            assert result == sample_drivers

            # Verify session_key was passed
            call_args = mock_get.call_args
            assert call_args[1]["params"]["session_key"] == 9158


class TestOpenF1ClientLaps:
    """Tests for the get_laps method."""

    def test_get_laps(self, api_client, sample_laps):
        """Test getting laps."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_laps
            mock_get.return_value = mock_response

            result = api_client.get_laps(session_key=9161)
            assert result == sample_laps

    def test_get_laps_with_driver(self, api_client, sample_laps):
        """Test getting laps filtered by driver."""
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_laps
            mock_get.return_value = mock_response

            result = api_client.get_laps(session_key=9161, driver_number=1)
            assert result == sample_laps

            # Verify driver_number was passed
            call_args = mock_get.call_args
            assert call_args[1]["params"]["driver_number"] == 1


class TestOpenF1ClientCarData:
    """Tests for the get_car_data method."""

    def test_get_car_data(self, api_client):
        """Test getting car data."""
        sample_car_data = [{"driver_number": 1, "speed": 320}]
        with patch("f1.client.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_car_data
            mock_get.return_value = mock_response

            result = api_client.get_car_data(session_key=9161)
            assert result == sample_car_data
