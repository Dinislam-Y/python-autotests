# How I Built the Framework

This note explains the reasoning behind the framework design in this repository.

It is not a generic "how to write tests" article. It is a description of how this specific project was put together, what constraints shaped it, and why I made the trade-offs that I did.

## Starting point

I did not want this repository to become a pile of test files with hardcoded selectors and repeated setup.

The project had to solve two different testing problems:

| Problem type | Target | Main risk |
| --- | --- | --- |
| UI testing | `cms-dev.tochka-school.ru` | Flaky selectors, hard-to-read flows |
| API testing | `reqres.in` | Shallow validation that stops at status codes |

I also wanted the structure to be interview-friendly. A reviewer should be able to open the repository and understand the architecture quickly.

## Main design goal

The primary goal was to keep each layer small and predictable.

Instead of putting selectors, actions, assertions, and fixtures into the same place, I split responsibilities into dedicated parts:

| Layer | Role |
| --- | --- |
| `locators` | Store selectors only |
| `pages` | Perform actions only |
| `checks` | Perform assertions only |
| `tests` | Describe scenario flow only |
| `conftest.py` | Assemble reusable fixtures |

This rule sounds strict, but it pays off when the suite grows.

## Why I reused a Flutter QA idea

The most important design choice in this repository came from my Flutter QA background.

In a large Flutter project, I had already seen what happens when tests mix too many responsibilities:

- selectors leak into tests
- assertions get buried inside helper methods
- page objects become too smart
- failures become harder to interpret

So I reused the same core idea in Python and adapted it to `pytest`, `Playwright`, and `requests`.

The result is not a one-to-one port from Flutter. It is the same discipline applied to a different stack.

## How the UI layer was built

For the UI side, I used a four-part flow:

1. `locators` define where elements live.
2. `pages` describe what the user does.
3. `checks` describe what must be true.
4. `tests` combine actions and expectations into readable scenarios.

### Why `pages` and `checks` are separate

This is the core architectural choice of the framework.

If a page object both clicks buttons and asserts outcomes, it becomes harder to reuse and harder to trust. A method like `open_page_and_verify_banner()` may feel convenient, but it hides too much behavior.

By contrast:

- `pages` tell the browser what to do
- `checks` tell the test what to verify

That separation makes failures easier to classify:

| Failure area | Usual meaning |
| --- | --- |
| Locator failure | The selector or DOM structure changed |
| Page action failure | Navigation or interaction is broken |
| Check failure | The page loaded, but the expected outcome is wrong |

### Why some navigation is direct by URL

In a perfect world, every navigation step would happen through the visible header menu.

In practice, public websites can change markup, lazy-load parts of the page, or hide links behind unstable front-end behavior. For some checks, going directly to a route is simply more reliable and keeps the test focused on the page under test instead of the menu implementation.

That is why this framework mixes two styles when it makes sense:

- real UI interaction for flows that should behave like a user journey
- direct route navigation for stable page accessibility checks

This is a pragmatic choice, not a dogma.

## How the API layer was built

The API side follows a simpler structure, but the same idea still applies: keep reusable logic out of test files.

### `ApiClient`

I introduced a small wrapper around `requests.Session` in `utils/api_client.py`.

It does three useful things:

| Concern | Why it exists |
| --- | --- |
| Base URL handling | Tests do not repeat host names everywhere |
| Shared session | Requests reuse a session instead of creating one each time |
| Allure attachments | API responses are visible in reports when debugging failures |

This wrapper is intentionally small. I did not want to build a fake SDK. I only wanted the minimum abstraction that makes tests cleaner.

### Response models

One of the easiest ways to make API tests look more mature is to validate response structure, not just status codes.

That is why the repository has `Pydantic` models in `tests/api/models.py`.

This helps in two ways:

- the tests document the expected response shape
- schema drift becomes visible immediately

For example, if an endpoint suddenly changes field names or types, parsing fails and the test tells you that the contract changed.

## Why fixtures matter here

`pytest` fixtures are the assembly layer of the framework.

They keep the tests short and prevent repeated object construction:

- `tests/conftest.py` exposes shared settings
- `tests/api/conftest.py` wires API client and API checks
- `tests/ui/conftest.py` wires page objects and UI checks

This is important because it keeps scenario files focused on behavior instead of setup noise.

## Reporting and debuggability

I wanted the framework to be readable in code and useful after failure.

That is why reporting was part of the design, not an afterthought.

### Allure was added for three reasons

| Reason | Example |
| --- | --- |
| Traceability | Named steps show what the test was doing |
| Faster debugging | API responses are attached automatically |
| UI evidence | Failed UI tests capture screenshots |

This matters in portfolio projects too. Good reporting makes the framework feel like a working engineering tool, not just a demo.

## Why there are no database checks

This project tests public targets. I do not control the backend or database behind them.

That means database verification would be fake in this repository. I could claim it as a feature, but it would not be honest engineering.

So I kept the scope realistic:

- external UI verification
- external API verification
- schema validation
- reporting
- reusable framework structure

If I wanted to demonstrate real database checks, I would add a small local service with a test database and then assert persistence directly. That would be a different expansion of the project, not a hidden capability of the current repo.

## Trade-offs I accepted

Every framework structure has trade-offs. This one does too.

| Trade-off | Why I accepted it |
| --- | --- |
| More files than a quick prototype | Better separation and easier scaling |
| Slightly more ceremony in tests | Cleaner scenario language |
| Direct-route navigation in some cases | Lower flakiness for page availability checks |
| Separate check classes | Better failure localization |

I prefer this trade-off profile for a framework project because maintainability matters more than short-term speed.

## What I would improve next

If I continue evolving this repository, these are the most logical next steps:

1. Strengthen contract validation across more API responses.
2. Add a CI matrix for multiple Python versions.
3. Add mocks and test doubles for isolated utility tests.
4. Expand architecture documentation with diagrams.

## Final principle

The framework was built around one rule:

Keep the test readable, keep the responsibilities separate, and make failures easy to understand.

That is the main idea behind every structural choice in this repository.
