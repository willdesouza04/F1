"""Command-line interface for F1 data."""

import json

import click

from .client import OpenF1Client
from .exceptions import OpenF1Error


@click.group()
def main():
    """F1 Data Client - Query OpenF1 API from the command line."""
    pass


@main.command()
@click.option("--year", type=int, help="Filter by year (e.g., 2024)")
@click.option("--limit", type=int, help="Limit number of results")
@click.option("--format", type=click.Choice(["json", "text"]), default="json")
def meetings(year, limit, format):
    """List Formula 1 meetings."""
    try:
        client = OpenF1Client()
        filters = {}
        if year:
            filters["year"] = year
        if limit:
            filters["limit"] = limit

        data = client.get_meetings(**filters)

        if format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            for meeting in data:
                click.echo(
                    f"{meeting.get('year', 'N/A')} - "
                    f"{meeting.get('meeting_name', 'N/A')} "
                    f"({meeting.get('location', 'N/A')})"
                )
    except OpenF1Error as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("--year", type=int, help="Filter by year")
@click.option("--limit", type=int, help="Limit number of results")
@click.option("--format", type=click.Choice(["json", "text"]), default="json")
def sessions(year, limit, format):
    """List Formula 1 sessions."""
    try:
        client = OpenF1Client()
        filters = {}
        if year:
            filters["year"] = year
        if limit:
            filters["limit"] = limit

        data = client.get_sessions(**filters)

        if format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            for session in data:
                click.echo(
                    f"Session {session.get('session_key', 'N/A')}: "
                    f"{session.get('session_name', 'N/A')} "
                    f"({session.get('session_type', 'N/A')})"
                )
    except OpenF1Error as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("--session", type=int, required=True, help="Session key (required)")
@click.option("--limit", type=int, help="Limit number of results")
@click.option("--format", type=click.Choice(["json", "text"]), default="json")
def drivers(session, limit, format):
    """List drivers for a session."""
    try:
        client = OpenF1Client()
        filters = {}
        if limit:
            filters["limit"] = limit

        data = client.get_drivers(session, **filters)

        if format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            for driver in data:
                click.echo(
                    f"#{driver.get('driver_number', 'N/A')}: "
                    f"{driver.get('first_name', 'N/A')} "
                    f"{driver.get('last_name', 'N/A')} "
                    f"({driver.get('team_name', 'N/A')})"
                )
    except OpenF1Error as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("--session", type=int, required=True, help="Session key (required)")
@click.option("--driver", type=int, help="Filter by driver number")
@click.option("--limit", type=int, help="Limit number of results")
@click.option("--format", type=click.Choice(["json", "text"]), default="json")
def laps(session, driver, limit, format):
    """List laps for a session."""
    try:
        client = OpenF1Client()
        filters = {}
        if driver:
            filters["driver_number"] = driver
        if limit:
            filters["limit"] = limit

        data = client.get_laps(session, **filters)

        if format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            for lap in data:
                click.echo(
                    f"Lap {lap.get('lap_number', 'N/A')}: "
                    f"{lap.get('duration_seconds', 'N/A')}s "
                    f"(Driver {lap.get('driver_number', 'N/A')})"
                )
    except OpenF1Error as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("--session", type=int, required=True, help="Session key (required)")
@click.option("--limit", type=int, help="Limit number of results")
@click.option("--format", type=click.Choice(["json", "text"]), default="json")
def car_data(session, limit, format):
    """Get car telemetry for a session."""
    try:
        client = OpenF1Client()
        filters = {}
        if limit:
            filters["limit"] = limit

        data = client.get_car_data(session, **filters)

        if format == "json":
            click.echo(json.dumps(data, indent=2))
        else:
            for entry in data:
                click.echo(
                    f"Driver {entry.get('driver_number', 'N/A')}: "
                    f"Speed {entry.get('speed', 'N/A')} "
                    f"(Lap {entry.get('lap_number', 'N/A')})"
                )
    except OpenF1Error as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
