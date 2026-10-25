"""Pytest configuration and shared fixtures."""

from unittest.mock import MagicMock, patch

import pytest

from f1.client import OpenF1Client


@pytest.fixture
def mock_client():
    """Fixture for a mocked OpenF1Client."""
    with patch("f1.client.requests.get") as mock_get:
        yield MagicMock(side_effect=mock_get), mock_get


@pytest.fixture
def sample_meetings():
    """Sample meeting data from OpenF1 API."""
    return [
        {
            "meeting_key": 1204,
            "year": 2024,
            "meeting_name": "Bahrain Grand Prix",
            "location": "Bahrain",
            "country_key": 84,
        },
        {
            "meeting_key": 1205,
            "year": 2024,
            "meeting_name": "Saudi Arabian Grand Prix",
            "location": "Saudi Arabia",
            "country_key": 216,
        },
    ]


@pytest.fixture
def sample_drivers():
    """Sample driver data from OpenF1 API."""
    return [
        {
            "driver_number": 1,
            "first_name": "Max",
            "last_name": "Verstappen",
            "team_name": "Red Bull",
            "session_key": 9158,
        },
        {
            "driver_number": 63,
            "first_name": "George",
            "last_name": "Russell",
            "team_name": "Mercedes",
            "session_key": 9158,
        },
    ]


@pytest.fixture
def sample_laps():
    """Sample lap data from OpenF1 API."""
    return [
        {
            "lap_number": 1,
            "driver_number": 1,
            "duration_seconds": 96.284,
            "session_key": 9161,
        },
        {
            "lap_number": 2,
            "driver_number": 1,
            "duration_seconds": 95.847,
            "session_key": 9161,
        },
    ]


@pytest.fixture
def api_client():
    """Fixture for OpenF1Client."""
    return OpenF1Client()
