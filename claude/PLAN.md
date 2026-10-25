# Plan: Setup e Estrutura Inicial do Projeto F1

## Context

O projeto **F1** é uma biblioteca Python com CLI para consumir dados da **OpenF1 API** (histórico de Fórmula 1 desde 2023). O projeto está em setup inicial e precisa seguir rigorosamente os padrões documentados em **SKILL.md** — que cobrem:
- Python versioning com Pyenv
- Dependency management com Poetry
- Code quality com Ruff
- Testing com Pytest (cobertura >=50%)
- Documentation com MkDocs Material
- CI/CD com GitHub Actions

**Decisões de Design:**
- **Escopo**: Biblioteca + CLI (ambos na mesma package)
- **HTTP Client**: Síncrono via `requests` (simples, suficiente para v1)
- **Modelos**: Raw dicts/JSON (sem Pydantic inicialmente, overhead mínimo)

**Objetivo**: Estruturar o projeto para desenvolvimento profissional, validação contínua e fácil manutenção, atendendo todos os critérios do SKILL.md.

---

## Implementation Phases

### Phase 1: Python Environment Setup
**Goal**: Lock Python version and initialize Poetry environment

**Tasks:**
1. Verify Pyenv is installed and functional (`pyenv --version`)
2. Install Python 3.13.x via Pyenv if not present (`pyenv install 3.13.x`)
3. Set Python 3.13.x as project version: create `.python-version` file at project root with `3.13.x`
4. Verify interpreter: `python --version` should show 3.13.x
5. Initialize Poetry virtual environment: `poetry install` (uses existing pyproject.toml)
6. Verify Poetry environment: `poetry shell` or `poetry run python --version`

**Critical Files:**
- `.python-version` (NEW) — declares Python 3.13.x for Pyenv
- `poetry.lock` (CREATED by poetry install) — locks all dependencies

**Verification:**
- `.python-version` exists and contains `3.13.x`
- `poetry lock` generates without errors
- `poetry show` lists all dependencies

---

### Phase 2: Project Configuration & Dependencies
**Goal**: Define metadata and all required tools in pyproject.toml

**Tasks:**
1. Update `pyproject.toml` metadata:
   - `description = "F1 data client and CLI for OpenF1 API"`
   - `authors = ["William Lacerda de Souza <willdesouza04@gmail.com>"]`
   - `license = "MIT"`
   - Keep `python = "^3.13"`

2. Add **production dependencies**:
   - `requests` (>=2.31.0) — HTTP client for API calls
   - `click` (>=8.0) — CLI framework for CLI commands

3. Add **development dependencies**:
   - `ruff` (>=0.6.0) — Linting and formatting
   - `pytest` (>=7.0) — Test framework
   - `pytest-cov` (>=4.0) — Coverage measurement
   - `mkdocs` (>=1.5) — Documentation builder
   - `mkdocs-material` (>=9.0) — Material theme for docs

4. Configure **[tool.ruff]** in pyproject.toml:
   - `line-length = 88`
   - `target-version = "py313"`
   - Include rules: E, W, F, I, N, UP, SIM (error, warning, pyflakes, import-sort, naming, upgrade, simplify)

5. Configure **[tool.pytest.ini_options]**:
   - `testpaths = ["tests"]`
   - `addopts = "--cov=src/f1 --cov-report=term-missing --cov-report=html --cov-fail-under=50"`

6. Configure **[tool.coverage.run]**:
   - `source = ["src/f1"]`
   - `branch = true`

7. Run `poetry lock` to generate/update `poetry.lock`

**Critical Files:**
- `pyproject.toml` (UPDATED) — all configuration, dependencies, tool settings

**Verification:**
- `poetry show` lists all production + dev dependencies
- `poetry lock` exists and is consistent
- `ruff --version` works (check via `poetry run ruff --version`)

---

### Phase 3: Repository Configuration
**Goal**: Create .gitignore and baseline documentation

**Tasks:**
1. Create `.gitignore`:
   ```
   # Virtual environments
   .venv/
   venv/
   ENV/
   
   # Python cache
   __pycache__/
   *.pyc
   *.pyo
   *.egg-info/
   dist/
   build/
   
   # Testing & Coverage
   .pytest_cache/
   .coverage
   htmlcov/
   .tox/
   
   # IDE & Editor
   .vscode/
   .idea/
   *.swp
   *.swo
   *~
   
   # Tools
   .ruff_cache/
   
   # Docs
   site/
   
   # Environment
   .env
   .env.local
   ```

2. Enhance `README.md`:
   - Project title and one-liner description
   - Features overview
   - Quick start (installation, usage example)
   - Links to full documentation, API reference
   - Contribution guidelines link

**Critical Files:**
- `.gitignore` (NEW) — excludes .venv, caches, build artifacts
- `README.md` (UPDATED) — user-facing overview

**Verification:**
- `git status` shows clean working tree
- `.venv` is not tracked by Git
- `poetry.lock` IS tracked

---

### Phase 4: Documentation Structure
**Goal**: Create documentation infrastructure with MkDocs Material

**Tasks:**
1. Create `mkdocs.yml` at project root:
   - `site_name: "F1 Data Client"`
   - `theme: material` with dark mode support
   - `nav` structure linking to docs sections
   - Include search plugin, code highlighting

2. Create `docs/` directory with skeleton pages:
   - `docs/index.md` — Overview, quick links, feature list
   - `docs/getting-started.md` — Installation, basic usage, Python 3.13 requirement
   - `docs/architecture.md` — Client design, module layout, endpoints supported
   - `docs/development.md` — How to run tests, lint, docs build; validation checklist
   - `docs/api-reference.md` — Client API, endpoint methods, query parameters, examples

3. Link all pages in mkdocs.yml nav

**Critical Files:**
- `mkdocs.yml` (NEW) — documentation configuration
- `docs/index.md`, `docs/getting-started.md`, etc. (NEW) — content pages

**Verification:**
- `poetry run mkdocs serve` runs without errors
- Pages are discoverable in nav
- `poetry run mkdocs build --strict` succeeds (no warnings)

---

### Phase 5: Core Module Implementation
**Goal**: Create HTTP client and CLI foundation

**Tasks:**
1. Update `src/f1/__init__.py`:
   - Export `__version__ = "0.1.0"`
   - Export `OpenF1Client` class
   - Export main CLI entry point

2. Create `src/f1/client.py`:
   - Class `OpenF1Client`:
     - Constructor: `__init__(base_url="https://api.openf1.org/v1", timeout=30)`
     - Methods for each endpoint (return dicts/JSON):
       - `get_car_data(session_key: int, **filters) -> list[dict]`
       - `get_drivers(session_key: int, **filters) -> list[dict]`
       - `get_laps(session_key: int, **filters) -> list[dict]`
       - `get_meetings(year: int = None, **filters) -> list[dict]`
       - `get_sessions(year: int = None, **filters) -> list[dict]`
       - (additional endpoints as needed)
     - Private method to build query params from filters
     - Error handling for HTTP errors (connection, timeouts, 4xx/5xx)

3. Create `src/f1/cli.py`:
   - Use `click` framework for commands
   - Command structure: `f1 <endpoint> [options]`
     - `f1 meetings --year 2024` → list meetings
     - `f1 drivers --session 9158` → list drivers
     - `f1 laps --session 9161 --driver 63` → list driver laps
   - Format output: JSON or table (CSV later)
   - Error messages and help text

4. Create `src/f1/exceptions.py`:
   - Base exception: `OpenF1Error`
   - Specific exceptions: `NetworkError`, `APIError`, `NotFoundError`

**Critical Files:**
- `src/f1/__init__.py` (UPDATED)
- `src/f1/client.py` (NEW) — HTTP client
- `src/f1/cli.py` (NEW) — CLI commands
- `src/f1/exceptions.py` (NEW) — error hierarchy

**Verification:**
- `from f1 import OpenF1Client` works
- `client = OpenF1Client()` initializes
- Methods exist and return dicts
- `f1 --help` shows CLI help

---

### Phase 6: Testing & Coverage
**Goal**: Establish test infrastructure, achieve >=50% coverage

**Tasks:**
1. Create `tests/conftest.py`:
   - Pytest fixtures for:
     - Mock OpenF1Client with hardcoded responses
     - Sample data from doc_api.md endpoints
     - Example: fixture `mock_client` returning fake data

2. Create `tests/test_client.py`:
   - Test `OpenF1Client` initialization
   - Test each endpoint method with mocked HTTP (use `unittest.mock.patch`)
   - Test query parameter building
   - Test error scenarios (connection timeout, 404, invalid JSON response)
   - Target: >=10 test cases covering critical paths

3. Create `tests/test_cli.py`:
   - Test CLI command parsing with `click.testing.CliRunner`
   - Test help text
   - Test integration with mocked client
   - Target: >=5 test cases

4. Run `poetry run pytest` to execute tests
5. Verify coverage: `poetry run pytest --cov=src/f1 --cov-report=term-missing`
   - Coverage must be >=50% of src/f1/
   - Report shows uncovered lines

**Critical Files:**
- `tests/__init__.py` (EXISTS)
- `tests/conftest.py` (NEW) — fixtures and mocks
- `tests/test_client.py` (NEW) — client tests
- `tests/test_cli.py` (NEW) — CLI tests

**Verification:**
- `pytest` shows all tests passing
- Coverage report shows >=50%
- Coverage HTML report generated in `htmlcov/`

---

### Phase 7: Validation Pipeline
**Goal**: Establish reproducible validation workflow (local + CI)

**Tasks:**
1. Create `DEVELOPMENT.md` documenting validation steps in order:
   ```
   1. Verify Python version: python --version (should be 3.13.x)
   2. Verify Poetry: poetry --version
   3. Install dependencies: poetry install
   4. Run lint: poetry run ruff check src/ tests/
   5. Check formatting: poetry run ruff format --check src/ tests/
   6. Run tests: poetry run pytest
   7. Check coverage: >= 50% (see pytest output)
   8. Build docs: poetry run mkdocs build --strict
   9. All steps must pass before commit
   ```

2. Optionally create a validation script (e.g., `scripts/validate.sh` or `scripts/validate.py`)

**Critical Files:**
- `DEVELOPMENT.md` (NEW) — validation procedure

**Verification:**
- Each step in sequence passes
- No linting issues
- All tests pass with >=50% coverage
- Documentation builds with no warnings

---

### Phase 8: GitHub Actions CI (Optional)
**Goal**: Automate validation on push/PR (if project scope includes)

**Tasks:**
1. Create `.github/workflows/ci.yml`:
   - Trigger on: push to main, all PRs
   - Steps:
     - Setup Python 3.13
     - Install Poetry
     - Run `poetry install`
     - Run `ruff check` and `ruff format --check`
     - Run `pytest --cov --cov-fail-under=50`
     - Run `mkdocs build --strict`
   - Fail if any step fails

**Note:** Defer this if not in initial scope. Can be added later without disrupting phases 1-7.

---

## Dependency Graph

```
Phase 1 (Pyenv/Poetry)
      ↓
Phase 2 (Dependencies/Config)
      ↓
Phase 3 (.gitignore) [can run in parallel with Phase 4]
Phase 4 (Documentation) [can run in parallel with Phase 3]
      ↓
Phase 5 (Core Implementation)
      ↓
Phase 6 (Testing & Coverage)
      ↓
Phase 7 (Validation)
      ↓
Phase 8 (CI/CD — optional)
```

---

## Critical Files Summary

| File | Action | Purpose |
|------|--------|---------|
| `.python-version` | CREATE | Declare Python 3.13.x for Pyenv |
| `pyproject.toml` | UPDATE | Dependencies, metadata, tool config |
| `poetry.lock` | CREATE | Locked dependencies (auto-generated) |
| `.gitignore` | CREATE | Exclude .venv, caches, artifacts |
| `README.md` | UPDATE | User-facing overview, quick start |
| `mkdocs.yml` | CREATE | Docs configuration |
| `docs/index.md` ... | CREATE | Documentation pages |
| `src/f1/__init__.py` | UPDATE | Package exports |
| `src/f1/client.py` | CREATE | OpenF1Client HTTP client |
| `src/f1/cli.py` | CREATE | CLI commands |
| `src/f1/exceptions.py` | CREATE | Error hierarchy |
| `tests/conftest.py` | CREATE | Pytest fixtures |
| `tests/test_client.py` | CREATE | Client unit tests |
| `tests/test_cli.py` | CREATE | CLI tests |
| `DEVELOPMENT.md` | CREATE | Development workflow docs |

---

## Verification Strategy

### Local Validation (Pre-Commit)
Execute in order:
```
1. python --version → 3.13.x
2. poetry show → all deps listed
3. poetry run ruff check src/ tests/ → 0 failures
4. poetry run ruff format --check src/ tests/ → no changes needed
5. poetry run pytest → all tests pass
6. poetry run pytest --cov=src/f1 → coverage >= 50%
7. poetry run mkdocs build --strict → no errors
```

### Checkpoint Tests After Each Phase
- **Phase 1**: `.python-version` exists, Python 3.13.x confirmed
- **Phase 2**: `poetry.lock` generated, dependencies installable
- **Phase 3**: `.gitignore` filters .venv, README informative
- **Phase 4**: `mkdocs serve` runs, pages load
- **Phase 5**: `import f1` works, client methods callable
- **Phase 6**: All tests pass, coverage >= 50%
- **Phase 7**: Full validation script succeeds
- **Phase 8**: GitHub Actions workflow passes on push

---

## SKILL.md Compliance Checklist

- [ ] Pyenv: `.python-version` created and versionable
- [ ] Poetry: `pyproject.toml` + `poetry.lock` configured and versionable
- [ ] Structure: Code in `src/f1/`, tests in `tests/`, docs in `docs/`
- [ ] Ruff: Configured in `pyproject.toml`, lint passes
- [ ] Pytest: Configured, all tests pass, fixtures in conftest.py
- [ ] Coverage: >=50% of `src/f1/` measured and reported
- [ ] MkDocs: Configured, builds in strict mode
- [ ] .gitignore: .venv, caches, artifacts excluded
- [ ] Validation: Full pipeline documented and reproducible
- [ ] CI/CD: GitHub Actions setup (if in scope)

---

## Next Steps

1. **Execute Phase 1-7 sequentially**, checkpoint after each
2. **If issues arise**, diagnose root cause (SKILL.md has detailed troubleshooting)
3. **Document blockers** if Pyenv, Poetry, or tool versions conflict
4. **Phase 8 (CI/CD)** can be deferred to after phases 1-7 are stable
5. **Long-term**: Expand client endpoints, add async support (httpx), add Pydantic models as API stabilizes
