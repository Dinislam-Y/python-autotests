import allure
import pytest

from tests.api.test_data import MISSING_PASSWORD_ERROR, VALID_EMAIL, VALID_PASSWORD

pytestmark = pytest.mark.api


@allure.feature("Auth API")
class TestAuth:
    """Регистрация и логин — reqres принимает только определённые email."""

    @allure.story("Регистрация")
    @allure.title("Успешная регистрация")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_successful(self, api_client, auth_checks):
        response = api_client.post("/api/register", json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
        auth_checks.check_register_success(response)

    @allure.story("Регистрация")
    @allure.title("Регистрация без пароля — ошибка 400")
    def test_register_missing_password(self, api_client, auth_checks):
        response = api_client.post("/api/register", json={"email": VALID_EMAIL})
        auth_checks.check_register_error(response, MISSING_PASSWORD_ERROR)

    @allure.story("Логин")
    @allure.title("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_successful(self, api_client, auth_checks):
        response = api_client.post("/api/login", json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
        auth_checks.check_login_success(response)

    @allure.story("Логин")
    @allure.title("Логин без пароля — ошибка 400")
    def test_login_missing_password(self, api_client, auth_checks):
        response = api_client.post("/api/login", json={"email": VALID_EMAIL})
        auth_checks.check_login_error(response, MISSING_PASSWORD_ERROR)
