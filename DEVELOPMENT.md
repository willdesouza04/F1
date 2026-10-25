# Development Guide — F1 Project

This document describes the development workflow and validation process for the F1 project.

## Setup

### Prerequisites

- Python 3.13+ (managed by Pyenv)
- Poetry for dependency management
- Git for version control

### Initial Setup

```bash
# 1. Verify Python is set to 3.13.x
python --version

# 2. Install project dependencies
poetry install

# 3. Activate the virtual environment (optional, Poetry handles it)
poetry shell
```

## Validation Process

All code must pass the following validation steps before being committed. Run them in order:

### 1. Verify Python Version

```bash
python --version
# Expected: Python 3.13.x
```

File: `.python-version`

### 2. Verify Poetry Environment

```bash
poetry --version
poetry show
```

All dependencies should be listed, including:
- **Production**: `requests`, `click`
- **Development**: `ruff`, `pytest`, `pytest-cov`, `mkdocs`, `mkdocs-material`

### 3. Check Code with Ruff (Lint)

```bash
poetry run ruff check src/ tests/
```

All checks must pass. Fix any issues with:

```bash
poetry run ruff check --fix src/ tests/
```

### 4. Check Formatting with Ruff

```bash
poetry run ruff format --check src/ tests/
```

If code needs formatting:

```bash
poetry run ruff format src/ tests/
```

### 5. Run Tests with Pytest

```bash
poetry run pytest
```

All tests must pass. For verbose output:

```bash
poetry run pytest -v
```

### 6. Check Test Coverage

```bash
poetry run pytest --cov=src/f1 --cov-report=term-missing
```

**Coverage must be ≥50%**. View the coverage report:

```bash
poetry run pytest --cov=src/f1 --cov-report=html
# Then open htmlcov/index.html in a browser
```

### 7. Build and Validate Documentation

```bash
poetry run mkdocs build --strict
```

Documentation must build without errors or warnings.

## Validation Checklist

Before committing, ensure all of these pass:

- [ ] `python --version` shows 3.13.x
- [ ] `poetry show` lists all dependencies
- [ ] `poetry run ruff check src/ tests/` → **All checks passed!**
- [ ] `poetry run ruff format --check src/ tests/` → **All files already formatted**
- [ ] `poetry run pytest` → **All tests passed**
- [ ] `poetry run pytest --cov=src/f1` → **≥50% coverage**
- [ ] `poetry run mkdocs build --strict` → **Build succeeded**

## Project Structure

```
src/f1/                # Main package
├── __init__.py       # Package exports
├── client.py         # OpenF1Client HTTP client
├── cli.py            # Click CLI commands
└── exceptions.py     # Custom exceptions

tests/                # Test suite
├── conftest.py       # Pytest fixtures & shared data
├── test_client.py    # Client unit tests
└── test_cli.py       # CLI command tests

docs/                 # Documentation (Markdown)
├── index.md
├── getting-started.md
├── architecture.md
├── api-reference.md
└── development.md

pyproject.toml        # Project config & dependencies
mkdocs.yml            # Documentation config
.python-version       # Pyenv version pin
.gitignore            # Git ignore rules
```

## Common Workflows

### Adding a New Endpoint

1. **Add method to `OpenF1Client`** in `src/f1/client.py`:

```python
def get_my_data(self, key: int, **filters) -> list[dict]:
    """Get my data from the API."""
    params = {"key": key, **filters}
    return self._fetch("/my_data", params)
```

2. **Add CLI command** in `src/f1/cli.py`:

```python
@main.command()
@click.option("--key", type=int, required=True)
def my_data(key):
    """Get my data."""
    client = OpenF1Client()
    data = client.get_my_data(key)
    click.echo(json.dumps(data, indent=2))
```

3. **Write tests** in `tests/test_client.py` and `tests/test_cli.py`

4. **Update documentation** in `docs/`

5. **Run full validation** before committing

### Running Only Specific Tests

```bash
# Run a single test file
poetry run pytest tests/test_client.py

# Run a specific test class
poetry run pytest tests/test_client.py::TestOpenF1ClientInit

# Run a specific test function
poetry run pytest tests/test_client.py::TestOpenF1ClientInit::test_init_with_defaults

# Run tests matching a pattern
poetry run pytest -k "meetings"

# Run with verbose output
poetry run pytest -v

# Run with detailed traceback
poetry run pytest --tb=long
```

### Viewing Documentation Locally

```bash
poetry run mkdocs serve
```

Then open `http://localhost:8000` in your browser. Changes are auto-reloaded.

## Dependencies

### Production Dependencies
- **requests** (≥2.31.0) — HTTP client for API calls
- **click** (≥8.0) — CLI framework

### Development Dependencies
- **ruff** (≥0.6.0) — Linting and formatting
- **pytest** (≥7.0) — Test framework
- **pytest-cov** (≥4.0) — Code coverage measurement
- **mkdocs** (≥1.5) — Documentation builder
- **mkdocs-material** (≥9.0) — Material theme

To add a dependency:

```bash
poetry add <package-name>              # Production
poetry add --group dev <package-name>  # Development
```

Then run:

```bash
poetry lock
poetry install
```

## Troubleshooting

### Python version not recognized

Ensure `.python-version` exists and contains `3.13.0`:

```bash
cat .python-version
# Should output: 3.13.0
```

If missing:

```bash
echo "3.13.0" > .python-version
pyenv local 3.13.0
```

### Poetry environment broken

Recreate the virtual environment:

```bash
rm -rf .venv
poetry install
poetry env use 3.13.0
```

### Tests fail with import errors

Ensure you're using Poetry's Python:

```bash
poetry run python -c "import f1; print(f1.__version__)"
```

### Coverage below 50%

Add more test cases. Check which lines are uncovered:

```bash
poetry run pytest --cov=src/f1 --cov-report=term-missing
```

Focus on covering the "Missing" lines.

### Documentation won't build

Check for broken links and invalid Markdown:

```bash
poetry run mkdocs build --strict -v
```

## Git Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make changes and run validation:
   ```bash
   # Make code changes...
   poetry run pytest
   # Run full validation (see Validation Checklist above)
   ```

3. Commit with a clear message:
   ```bash
   git add .
   git commit -m "Add my feature"
   ```

4. Push and create a PR:
   ```bash
   git push origin feature/my-feature
   # Create PR on GitHub
   ```

5. Ensure CI/CD passes on the PR

## Performance Tips

- **Faster lint checks**: Run Ruff on specific files instead of the entire project
- **Faster tests**: Run only affected test files or use `-k` pattern matching
- **Faster docs**: Use `mkdocs serve` for live preview instead of rebuilding

## Getting Help

- **Ruff rules**: `poetry run ruff rule <CODE>` (e.g., `poetry run ruff rule F401`)
- **Pytest help**: `poetry run pytest --help`
- **Click help**: `poetry run f1 --help`
- **MkDocs help**: `poetry run mkdocs --help`
