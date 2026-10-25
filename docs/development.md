# Development Guide

## Setup

### Prerequisites

- Python 3.13+
- Pyenv (for version management)
- Poetry (for dependency management)

### Initial Setup

1. **Verify Python version:**
   ```bash
   python --version  # Should be Python 3.13.x
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```
   Or run commands prefixed with `poetry run`.

## Development Workflow

### Code Style & Linting

This project uses **Ruff** for linting and formatting.

```bash
# Check code
poetry run ruff check src/ tests/

# Auto-fix issues
poetry run ruff check --fix src/ tests/

# Format code
poetry run ruff format src/ tests/

# Check formatting without changes
poetry run ruff format --check src/ tests/
```

### Testing

Tests are managed with **Pytest** and **pytest-cov**.

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=src/f1 --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_client.py

# Run with verbose output
poetry run pytest -v

# Open HTML coverage report
# After running tests, open htmlcov/index.html in a browser
```

**Coverage Requirements:**
- Minimum: 50% of `src/f1/` code
- Currently: Check `pytest` output for exact percentage

### Documentation

Documentation uses **MkDocs Material**.

```bash
# Build and serve locally (watch mode)
poetry run mkdocs serve

# Build static site
poetry run mkdocs build --strict

# Check for errors/warnings
poetry run mkdocs build --strict
```

Documentation files are in `docs/` (Markdown format).

## Validation Checklist

Before committing, run this full validation sequence:

```bash
# 1. Verify Python version
python --version

# 2. Check poetry environment
poetry --version
poetry show

# 3. Lint and format
poetry run ruff check src/ tests/
poetry run ruff format --check src/ tests/

# 4. Run tests
poetry run pytest

# 5. Check coverage (must be >= 50%)
poetry run pytest --cov=src/f1 --cov-report=term-missing

# 6. Build docs
poetry run mkdocs build --strict
```

All steps must pass before committing.

## Project Structure

```
src/f1/                 # Main package
├── __init__.py        # Package initialization
├── client.py          # OpenF1Client
├── cli.py             # CLI commands
└── exceptions.py      # Custom exceptions

tests/                 # Test suite
├── conftest.py        # Pytest fixtures
├── test_client.py     # Client tests
└── test_cli.py        # CLI tests
```

## Adding a New Endpoint

1. **Add method to `OpenF1Client`** in `src/f1/client.py`:
   ```python
   def get_my_data(self, key: int, **filters) -> list[dict]:
       """Get my data from the API."""
       endpoint = f"/my_data"
       params = {"key": key, **filters}
       return self._fetch(endpoint, params)
   ```

2. **Add corresponding CLI command** in `src/f1/cli.py`:
   ```python
   @main.command()
   @click.option("--key", type=int, required=True)
   def my_data(key):
       """Fetch my data."""
       client = OpenF1Client()
       data = client.get_my_data(key)
       click.echo(json.dumps(data, indent=2))
   ```

3. **Write tests** in `tests/test_client.py` and `tests/test_cli.py`

4. **Update documentation** in `docs/`

5. **Ensure coverage >= 50%**

## Git Workflow

1. Create a branch for your work
2. Make changes and pass all validation checks
3. Commit with clear messages
4. Push and create a PR
5. Ensure CI/CD passes

## Common Commands

| Command | Purpose |
|---------|---------|
| `poetry install` | Install all dependencies |
| `poetry run pytest` | Run tests |
| `poetry run ruff check src/ tests/` | Lint code |
| `poetry run ruff format src/ tests/` | Format code |
| `poetry run mkdocs serve` | View docs locally |
| `poetry show` | List all dependencies |
| `poetry lock` | Update poetry.lock |

## Troubleshooting

### Tests fail with import errors

Ensure Poetry environment is activated:
```bash
poetry shell
# Then run tests
pytest
```

### Linting shows errors I can't fix

Some errors may need manual review. Read the Ruff documentation:
```bash
poetry run ruff rule <RULE_CODE>
```

### MkDocs build fails

Check for broken links or invalid Markdown:
```bash
poetry run mkdocs build --strict -v
```

### Coverage below 50%

Add more tests covering the uncovered lines. Check the coverage report:
```bash
poetry run pytest --cov=src/f1 --cov-report=term-missing
# Or view HTML report:
# htmlcov/index.html
```

## Contributing

All contributions must:
- Pass linting (`ruff check`)
- Pass formatting (`ruff format --check`)
- Pass tests (`pytest`)
- Maintain >=50% coverage
- Update documentation

See the main README for contribution guidelines.
