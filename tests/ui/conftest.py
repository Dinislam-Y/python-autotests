import allure
import pytest
from playwright.sync_api import Page

from tests.ui.checks.courses_checks import CoursesChecks
from tests.ui.checks.footer_checks import FooterChecks
from tests.ui.checks.form_checks import FormChecks
from tests.ui.checks.header_checks import HeaderChecks
from tests.ui.checks.main_page_checks import MainPageChecks
from tests.ui.pages.courses_page import CoursesPage
from tests.ui.pages.footer_page import FooterPage
from tests.ui.pages.form_page import FormPage
from tests.ui.pages.header_page import HeaderPage
from tests.ui.pages.main_page import MainPage


# --- page objects ---

@pytest.fixture
def main_page(page: Page) -> MainPage:
    return MainPage(page)


@pytest.fixture
def header_page(page: Page) -> HeaderPage:
    return HeaderPage(page)


@pytest.fixture
def courses_page(page: Page) -> CoursesPage:
    return CoursesPage(page)


@pytest.fixture
def form_page(page: Page) -> FormPage:
    return FormPage(page)


@pytest.fixture
def footer_page(page: Page) -> FooterPage:
    return FooterPage(page)


# --- checks ---

@pytest.fixture
def main_page_checks(page: Page) -> MainPageChecks:
    return MainPageChecks(page)


@pytest.fixture
def header_checks(page: Page) -> HeaderChecks:
    return HeaderChecks(page)


@pytest.fixture
def courses_checks(page: Page) -> CoursesChecks:
    return CoursesChecks(page)


@pytest.fixture
def form_checks(page: Page) -> FormChecks:
    return FormChecks(page)


@pytest.fixture
def footer_checks(page: Page) -> FooterChecks:
    return FooterChecks(page)


# --- скриншот при падении ---

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Если UI-тест упал — делаю скриншот и прикладываю в allure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
