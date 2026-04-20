# Python QA Autotests

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC)
![Playwright](https://img.shields.io/badge/playwright-ui%20tests-45BA4B)
![Requests](https://img.shields.io/badge/requests-api%20tests-20232A)
![Allure](https://img.shields.io/badge/allure-reporting-orange)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)

UI and API test automation framework built with `pytest`, `Playwright`, `requests`, `Pydantic`, `Allure`, and `Docker`.

This repository covers two public targets:

| Area | Target | Purpose |
| --- | --- | --- |
| UI | `https://cms-dev.tochka-school.ru` | End-to-end checks for a real educational landing page |
| API | `https://reqres.in` | API flows, negative cases, and response schema validation |

The framework is based on a separation-of-concerns pattern I previously used in large Flutter QA projects and adapted for Python:

`Locators -> Pages -> Checks -> Tests`

The goal is simple: keep tests readable, make failures easier to localize, and avoid mixing navigation, assertions, and selectors in the same place.

## Table of Contents

- [Why this project exists](#why-this-project-exists)
- [What is inside](#what-is-inside)
- [Architecture](#architecture)
- [Project layout](#project-layout)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Run commands](#run-commands)
- [Docker](#docker)
- [Allure reporting](#allure-reporting)
- [Design decisions](#design-decisions)
- [Roadmap](#roadmap)

## Why this project exists

This is a portfolio-grade automation project with two goals:

1. Show a practical Python QA stack across UI and API testing.
2. Demonstrate framework design, not just isolated test scripts.

Instead of putting everything directly into test files, the project keeps reusable logic in dedicated layers and uses fixtures to compose scenarios cleanly.

## What is inside

### At a glance

| Metric | Current state |
| --- | --- |
| Python version | `3.9+` |
| Collected test cases | `60` |
| UI style | Page Object + dedicated checks layer |
| API style | Session-based client + strict contract validation |
| Reporting | Allure steps, attachments, screenshots on failure |
| Environment | Local venv or Docker |

### Test suite breakdown

| Suite | Scope | Collected cases |
| --- | --- | ---: |
| API: Users | CRUD user flows on `reqres.in` | 7 |
| API: Auth | Registration and login, positive and negative | 4 |
| API: Resources | Parameterized resource and pagination checks | 6 |
| UI: Navigation | Section navigation, logo behavior, browser history | 14 |
| UI: Main page | Hero, categories, directions, reviews, CTA blocks | 7 |
| UI: Courses | Catalog page, titles, subject routes | 8 |
| UI: Enrollment form | Modal visibility and input behavior | 5 |
| UI: Footer | Social links, documents, footer visibility | 6 |
| UI: User flows | Multi-step user journeys | 3 |
| Total | API + UI | 60 |

## Architecture

### Layer responsibilities

| Layer | Responsibility | What does not belong here |
| --- | --- | --- |
| `locators/` | Raw selectors and element addresses | Business logic, assertions |
| `pages/` | Actions such as open, click, fill, navigate, scroll | Assertions about expected results |
| `checks/` | Assertions and validation helpers | Direct navigation and UI actions |
| `test_*.py` | Scenario flow orchestration | Selectors, heavy logic, duplicated asserts |
| `conftest.py` | Fixture wiring and shared setup | Business-specific test logic |

### Why this split works

| Problem in test automation | How this project handles it |
| --- | --- |
| Tests become unreadable when selectors live everywhere | Selectors are isolated in `locators/` |
| Assertions get mixed into action methods | Assertions live in `checks/` only |
| Failures are hard to debug | The failing layer usually tells you where the issue is |
| Shared setup gets copied between test files | Fixtures build reusable page/check objects |
| API tests often stop at `status_code == 200` | `Pydantic` models validate response structure |

### API contract validation

The API layer validates more than business fields.

| Contract check | What it protects |
| --- | --- |
| `status_code` validation | Detects wrong response status early |
| JSON `Content-Type` validation | Catches format drift |
| Pydantic schema validation | Verifies field names and types |
| Empty `{}` validation for `404` | Verifies negative-case contract |
| Empty body validation for `204` | Verifies delete contract |
| `_meta` schema validation | Detects live `reqres.in` contract changes |

This matters because `reqres.in` now includes a service `_meta` block in successful responses. The project validates that block explicitly instead of ignoring it.

### Example flow

```python
def test_main_page_opens(main_page, main_page_checks, header_page):
    main_page.open()
    main_page_checks.check_title_contains(MAIN_PAGE_TITLE_CONTAINS)

    header_page.scroll_to_bottom()
    header_page.scroll_to_top()

    main_page_checks.check_hero_banner_visible()
```

The test reads like a scenario:

- open the page
- perform user actions
- verify outcomes through dedicated checks

### Architecture note

The full write-up is here:

- [How I built the framework](docs/how-i-built-the-framework.md)

## Project layout

```text
python-autotests/
|-- config/
|   |-- .env.example
|   `-- config.py
|-- docs/
|   `-- how-i-built-the-framework.md
|-- tests/
|   |-- conftest.py
|   |-- api/
|   |   |-- checks/
|   |   |-- conftest.py
|   |   |-- models.py
|   |   |-- test_data.py
|   |   |-- test_register.py
|   |   |-- test_resources.py
|   |   `-- test_users.py
|   `-- ui/
|       |-- checks/
|       |-- locators/
|       |-- pages/
|       |-- conftest.py
|       |-- test_courses.py
|       |-- test_data.py
|       |-- test_enrollment_form.py
|       |-- test_footer.py
|       |-- test_main_page.py
|       |-- test_navigation.py
|       `-- test_user_flow.py
|-- utils/
|   |-- api_client.py
|   `-- helpers.py
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
`-- README.md
```

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/Dinislam-Y/python-autotests.git
cd python-autotests

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
playwright install chromium
```

### 2. Configure environment variables

`reqres.in` requires a free API key.

```bash
cp config/.env.example .env
```

Then update `.env`:

```env
BASE_URL_UI=https://cms-dev.tochka-school.ru
BASE_URL_API=https://reqres.in
API_KEY=your-api-key-here
BROWSER=chromium
HEADLESS=true
TIMEOUT=30000
```

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL_UI` | `https://cms-dev.tochka-school.ru` | Base URL for UI tests |
| `BASE_URL_API` | `https://reqres.in` | Base URL for API tests |
| `API_KEY` | empty | API key required by `reqres.in` |
| `BROWSER` | `chromium` | Playwright browser selection |
| `HEADLESS` | `true` | Run UI tests headless or headed |
| `TIMEOUT` | `30000` | Default timeout in milliseconds |

## Run commands

### Local runs

| Command | What it does |
| --- | --- |
| `.venv/bin/pytest` | Run the full suite |
| `.venv/bin/pytest -m api` | Run API tests only |
| `.venv/bin/pytest -m ui` | Run UI tests only |
| `.venv/bin/pytest -m smoke` | Run smoke tests only |
| `.venv/bin/pytest tests/ui/test_navigation.py -v --headed` | Run one UI module in headed mode |
| `.venv/bin/pytest tests/api/test_users.py -v` | Run one API module |
| `.venv/bin/pytest --collect-only -q` | Show collected tests without execution |

### Pytest markers

| Marker | Meaning |
| --- | --- |
| `api` | API tests against `reqres.in` |
| `ui` | UI tests against the landing page |
| `smoke` | Small high-value subset |

## Docker

The repository also runs inside a container based on the official Microsoft Playwright Python image.

### Build and run

```bash
docker compose up --build
```

### What Docker gives you

| Benefit | Why it matters |
| --- | --- |
| Reproducible environment | Same Python, Playwright, and browser setup |
| Faster onboarding | No need to install the full toolchain manually |
| Shared execution model | Useful for demos and CI pipelines |

### Notes

- The container expects `.env` to exist.
- `allure-results/` is mounted back to the host machine.
- Headed UI mode is not the default Docker path; use headless execution there.

## Allure reporting

Allure output is enabled via `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-v --tb=short --alluredir=allure-results"
```

### Generate a report locally

```bash
allure serve allure-results
```

### Reporting features used in this project

| Feature | Where it is used |
| --- | --- |
| Test steps | Decorators on page and check methods |
| API attachments | `utils/api_client.py` stores response payloads |
| UI screenshots on failure | `tests/ui/conftest.py` hook attaches screenshots |

### API verification status

The current API contract layer has been verified against the live `reqres.in` service:

- `.venv/bin/pytest tests/api/ -q`
- result: `17 passed`

## Design decisions

### Why `Pages` and `Checks` are separate

In many UI test projects, page objects gradually turn into a mix of actions and assertions. That makes them convenient at first and painful later. This repository keeps them separate on purpose:

- a page object performs actions
- a check object validates outcomes
- a test composes both into a scenario

### Why the API layer uses models

The API tests do not stop at checking status codes. They validate JSON structure through `Pydantic` models, which makes schema drift visible earlier.

The contract layer also checks response shape details such as JSON `Content-Type`, empty-body behavior for `204`, and empty JSON behavior for `404`.

### Why there are no database checks

This project tests public external systems. There is no access to their internal databases, so database assertions would be artificial here. The current framework focuses on what can be verified honestly from the outside:

- UI behavior
- API responses
- response contracts
- navigation and user flows

## Roadmap

These are the most relevant next improvements for the current project:

| Next step | Why it matters |
| --- | --- |
| CI matrix | Run the suite across multiple Python versions |
| Mocks and test doubles | Add isolated tests for reusable utilities such as `ApiClient` |
| Architecture diagrams | Make framework decisions even easier to review visually |
| Broader API endpoint coverage | Extend the same contract rules to more endpoints or a local demo API |

## Related notes

- [Architecture note: How I built the framework](docs/how-i-built-the-framework.md)
- [Learning notes](learning/)
