# API Reference

## OpenF1Client

### Constructor

```python
OpenF1Client(base_url="https://api.openf1.org/v1", timeout=30)
```

**Parameters:**
- `base_url` (str): Base URL for OpenF1 API. Default: `https://api.openf1.org/v1`
- `timeout` (int): Request timeout in seconds. Default: `30`

**Returns:** `OpenF1Client` instance

### Methods

#### `get_meetings(year=None, **filters) -> list[dict]`

Get Formula 1 meetings (races, testing, etc.).

**Parameters:**
- `year` (int, optional): Filter by year (e.g., 2024)
- `**filters`: Additional query parameters passed to the API

**Returns:** List of meeting dictionaries

**Example:**
```python
client = OpenF1Client()

# All meetings
all_meetings = client.get_meetings()

# Meetings for 2024
meetings_2024 = client.get_meetings(year=2024)
```

**Response Example:**
```python
{
    "meeting_key": 1204,
    "year": 2024,
    "meeting_name": "Bahrain Grand Prix",
    "location": "Bahrain",
    "country_key": 84,
    "country_name": "Bahrain"
}
```

---

#### `get_sessions(year=None, **filters) -> list[dict]`

Get Formula 1 sessions (practice, qualifying, race).

**Parameters:**
- `year` (int, optional): Filter by year
- `**filters`: Additional query parameters

**Returns:** List of session dictionaries

**Example:**
```python
# Sessions for 2024
sessions_2024 = client.get_sessions(year=2024)

# Sessions by meeting key
sessions = client.get_sessions(meeting_key=1204)
```

---

#### `get_drivers(session_key, **filters) -> list[dict]`

Get drivers participating in a session.

**Parameters:**
- `session_key` (int): Session key (required)
- `**filters`: Additional query parameters

**Returns:** List of driver dictionaries

**Example:**
```python
# Drivers in session 9158
drivers = client.get_drivers(session_key=9158)

for driver in drivers:
    print(f"{driver['first_name']} {driver['last_name']}")
```

---

#### `get_laps(session_key, **filters) -> list[dict]`

Get lap times for a session.

**Parameters:**
- `session_key` (int): Session key (required)
- `**filters`: Additional query parameters (e.g., `driver_number=63`)

**Returns:** List of lap dictionaries

**Example:**
```python
# All laps in session 9161
laps = client.get_laps(session_key=9161)

# Laps for driver #63
driver_laps = client.get_laps(session_key=9161, driver_number=63)

# Check lap times
for lap in driver_laps[:5]:
    print(f"Lap {lap['lap_number']}: {lap['duration_seconds']}s")
```

---

#### `get_car_data(session_key, **filters) -> list[dict]`

Get car telemetry/data for a session.

**Parameters:**
- `session_key` (int): Session key (required)
- `**filters`: Additional query parameters

**Returns:** List of car data dictionaries

**Example:**
```python
# Car data for session 9161
car_data = client.get_car_data(session_key=9161)

# Filter by driver
driver_data = client.get_car_data(session_key=9161, driver_number=63)
```

---

## Exceptions

### OpenF1Error

Base exception for all F1 library errors.

```python
try:
    client.get_meetings()
except OpenF1Error as e:
    print(f"Error: {e}")
```

### NetworkError

Raised for connection/timeout errors.

```python
from f1.exceptions import NetworkError

try:
    client.get_meetings()
except NetworkError as e:
    print(f"Connection failed: {e}")
```

### APIError

Raised for API errors (4xx/5xx).

```python
from f1.exceptions import APIError

try:
    client.get_drivers(session_key=999999)
except APIError as e:
    print(f"API error: {e}")
```

### NotFoundError

Raised for 404 Not Found responses.

```python
from f1.exceptions import NotFoundError

try:
    client.get_drivers(session_key=999999)
except NotFoundError as e:
    print(f"Resource not found: {e}")
```

---

## Common Filters

Many methods accept `**filters` for query parameters:

```python
# Year filter
client.get_meetings(year=2024)

# Driver filter
client.get_laps(session_key=9158, driver_number=63)

# Limit results (API-specific)
client.get_meetings(limit=5)
```

Refer to [OpenF1 API documentation](https://www.openf1.org/) for all available filters.

---

## Timeouts

Customize request timeout globally:

```python
client = OpenF1Client(timeout=60)  # 60 second timeout
```

The default timeout is 30 seconds. Increase for slow connections or large responses.
