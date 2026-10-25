# F1 Data Client

Welcome to the F1 Data Client documentation! This is a Python library and command-line tool for accessing historical Formula 1 data from the [OpenF1 API](https://www.openf1.org/).

## Features

- **Synchronous HTTP Client**: Simple, synchronous wrapper around the OpenF1 API
- **CLI Tool**: Query F1 data directly from your terminal
- **Raw JSON Data**: Work with dictionaries and JSON directly — no heavy schemas
- **Python 3.13+**: Built for the latest Python version
- **Fully Tested**: 50%+ test coverage

## Quick Links

- **[Getting Started](getting-started.md)** — Install and run your first query
- **[Architecture](architecture.md)** — Understand the project structure
- **[API Reference](api-reference.md)** — Full endpoint documentation
- **[Development Guide](development.md)** — Set up your dev environment

## What is OpenF1?

[OpenF1](https://www.openf1.org/) provides historical Formula 1 data including:
- Meetings (races and sessions)
- Drivers and teams
- Lap times and telemetry
- Car data and positioning

Data is available from 2023 onwards.

## Quick Example

=== "Library"

    ```python
    from f1 import OpenF1Client
    
    client = OpenF1Client()
    meetings = client.get_meetings(year=2024)
    for meeting in meetings:
        print(f"{meeting['meeting_name']}")
    ```

=== "CLI"

    ```bash
    f1 meetings --year 2024
    ```

---

**Python 3.13+** | **MIT License** | [GitHub](https://github.com)
