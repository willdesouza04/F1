"""Tests for the CLI."""

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from f1.cli import main
from f1.exceptions import APIError, NetworkError


@pytest.fixture
def runner():
    """Fixture for Click CLI test runner."""
    return CliRunner()


class TestCLIMain:
    """Tests for the main CLI group."""

    def test_cli_help(self, runner):
        """Test that CLI help works."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "F1 Data Client" in result.output


class TestCLIMeetings:
    """Tests for the meetings command."""

    def test_meetings_command(self, runner, sample_meetings):
        """Test meetings command."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_meetings.return_value = sample_meetings
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["meetings"])
            assert result.exit_code == 0
            assert "Bahrain" in result.output

    def test_meetings_with_year(self, runner, sample_meetings):
        """Test meetings command with year filter."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_meetings.return_value = sample_meetings
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["meetings", "--year", "2024"])
            assert result.exit_code == 0
            mock_client.get_meetings.assert_called_once()

    def test_meetings_with_error(self, runner):
        """Test meetings command with API error."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_meetings.side_effect = APIError("API Error")
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["meetings"])
            assert result.exit_code == 1
            assert "Error" in result.output


class TestCLISessions:
    """Tests for the sessions command."""

    def test_sessions_command(self, runner):
        """Test sessions command."""
        sample_sessions = [{"session_key": 9158, "session_name": "Practice 1"}]
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_sessions.return_value = sample_sessions
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["sessions"])
            assert result.exit_code == 0


class TestCLIDrivers:
    """Tests for the drivers command."""

    def test_drivers_command_no_session(self, runner):
        """Test drivers command without required session option."""
        result = runner.invoke(main, ["drivers"])
        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output

    def test_drivers_command_with_session(self, runner, sample_drivers):
        """Test drivers command with session."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_drivers.return_value = sample_drivers
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["drivers", "--session", "9158"])
            assert result.exit_code == 0
            assert "Verstappen" in result.output or "Russell" in result.output

    def test_drivers_with_network_error(self, runner):
        """Test drivers command with network error."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_drivers.side_effect = NetworkError("Connection failed")
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["drivers", "--session", "9158"])
            assert result.exit_code == 1
            assert "Error" in result.output


class TestCLILaps:
    """Tests for the laps command."""

    def test_laps_command_no_session(self, runner):
        """Test laps command without required session option."""
        result = runner.invoke(main, ["laps"])
        assert result.exit_code != 0

    def test_laps_command_with_session(self, runner, sample_laps):
        """Test laps command with session."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_laps.return_value = sample_laps
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["laps", "--session", "9161"])
            assert result.exit_code == 0

    def test_laps_with_driver_filter(self, runner, sample_laps):
        """Test laps command with driver filter."""
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_laps.return_value = sample_laps
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["laps", "--session", "9161", "--driver", "1"])
            assert result.exit_code == 0
            mock_client.get_laps.assert_called_once()


class TestCLICarData:
    """Tests for the car_data command."""

    def test_car_data_command_no_session(self, runner):
        """Test car_data command without required session option."""
        result = runner.invoke(main, ["car-data"])
        assert result.exit_code != 0

    def test_car_data_command_with_session(self, runner):
        """Test car_data command with session."""
        sample_car_data = [{"driver_number": 1, "speed": 320}]
        with patch("f1.cli.OpenF1Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_car_data.return_value = sample_car_data
            mock_client_class.return_value = mock_client

            result = runner.invoke(main, ["car-data", "--session", "9161"])
            assert result.exit_code == 0
