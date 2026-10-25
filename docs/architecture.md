# Architecture

## Project Structure

```
f1/
├── src/f1/                 # Main package
│   ├── __init__.py         # Package exports
│   ├── client.py           # OpenF1Client HTTP client
│   ├── cli.py              # Click CLI commands
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite
│   ├── conftest.py         # Pytest fixtures
│   ├── test_client.py      # Client tests
│   └── test_cli.py         # CLI tests
├── docs/                   # Documentation (Markdown)
├── pyproject.toml          # Poetry configuration
├── mkdocs.yml              # MkDocs configuration
├── .python-version         # Pyenv Python version
├── .gitignore              # Git ignore rules
└── README.md               # Project overview
```

## Core Modules

### `f1.client.OpenF1Client`

Synchronous HTTP client for the OpenF1 API.

**Key Methods:**
- `get_meetings(year=None, **filters)` → `list[dict]`
- `get_drivers(session_key, **filters)` → `list[dict]`
- `get_laps(session_key, **filters)` → `list[dict]`
- `get_car_data(session_key, **filters)` → `list[dict]`
- `get_sessions(year=None, **filters)` → `list[dict]`

**Constructor:**
```python
OpenF1Client(base_url="https://api.openf1.org/v1", timeout=30)
```

### `f1.cli`

Click-based command-line interface.

**Commands:**
- `f1 meetings [--year YEAR]`
- `f1 drivers --session SESSION_KEY [--limit N]`
- `f1 laps --session SESSION_KEY [--driver DRIVER_NUMBER] [--limit N]`
- `f1 car-data --session SESSION_KEY [--limit N]`
- `f1 sessions [--year YEAR] [--limit N]`

### `f1.exceptions`

Error hierarchy for API and network errors.

**Exceptions:**
- `OpenF1Error` — Base exception
- `NetworkError` — Connection/timeout issues
- `APIError` — 4xx/5xx HTTP errors
- `NotFoundError` — 404 responses

## Data Model

Data is returned as plain Python dictionaries (JSON). No dataclass or Pydantic models are used initially to keep the library lightweight.

**Example Response:**
```python
{
    "meeting_key": 1204,
    "year": 2024,
    "location": "Bahrain",
    "country_key": 84
}
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Synchronous HTTP | Simple for v1, sufficient for most use cases |
| Raw dicts/JSON | Minimal overhead, flexible for schema changes |
| Click for CLI | Mature, well-documented, widely used |
| Requests library | Stable, synchronous HTTP standard |
| 50%+ test coverage | Validates core paths without exhaustiveness |

## Data Flow

```
User CLI Command
      ↓
Click Command Handler (cli.py)
      ↓
OpenF1Client method (client.py)
      ↓
HTTP Request (requests library)
      ↓
OpenF1 API
      ↓
JSON Response
      ↓
Parse & return dict
      ↓
Format & display (CLI) or return (library)
```

## Future Enhancements

- **Async support** (httpx or aiohttp)
- **Pydantic models** for type safety
- **Response caching**
- **Batch endpoints**
