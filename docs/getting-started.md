# Getting Started

## Requirements

- **Python 3.13+** (check with `python --version`)
- `pip` or `poetry` for package management

## Installation

### Using pip

```bash
pip install f1
```

### Using Poetry

```bash
poetry add f1
```

## First Query

### Library Usage

```python
from f1 import OpenF1Client

# Create a client (uses https://api.openf1.org/v1 by default)
client = OpenF1Client()

# Get all meetings for a year
meetings = client.get_meetings(year=2024)
print(f"Found {len(meetings)} meetings in 2024")

# Get drivers for a specific session
drivers = client.get_drivers(session_key=9158)
for driver in drivers:
    print(f"  - {driver['first_name']} {driver['last_name']} (#{driver['driver_number']})")
```

### CLI Usage

```bash
# List meetings for 2024
f1 meetings --year 2024

# List drivers in a session
f1 drivers --session 9158

# List laps for a driver
f1 laps --session 9161 --driver 63 --limit 10

# Output as JSON
f1 meetings --year 2024 --format json
```

## Next Steps

- Read the [API Reference](api-reference.md) for all available endpoints
- Check [Architecture](architecture.md) to understand the code structure
- See [Development](development.md) for contributing or customizing

## Troubleshooting

### ModuleNotFoundError: No module named 'f1'

Ensure the package is installed:
```bash
pip install f1
# or
poetry add f1
```

### Connection errors

Verify internet connectivity and that [api.openf1.org](https://api.openf1.org) is reachable.

### Invalid session_key

Session keys are numbers specific to meetings. Use `f1 meetings` to find valid session keys for a year.
