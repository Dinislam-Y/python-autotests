import pytest

from tests.api.checks.auth_checks import AuthChecks
from tests.api.checks.user_checks import UserChecks
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client(settings):
    """HTTP-клиент на всю сессию — переиспользуем соединение."""
    return ApiClient(settings.base_url_api, api_key=settings.api_key)


@pytest.fixture
def user_checks():
    return UserChecks()


@pytest.fixture
def auth_checks():
    return AuthChecks()
