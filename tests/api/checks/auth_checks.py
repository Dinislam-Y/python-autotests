import allure
from requests import Response

from tests.api.checks.base_api_checks import BaseApiChecks
from tests.api.models import ErrorResponse, LoginResponse, RegisterResponse


class AuthChecks(BaseApiChecks):
    """Проверки для /api/register и /api/login."""

    @allure.step("Проверка: регистрация успешна")
    def check_register_success(self, response: Response):
        data = self.validate_response_model(response, 200, RegisterResponse)
        assert data.token, "Токен пустой после регистрации"
        assert data.id, "id пустой после регистрации"

    @allure.step("Проверка: ошибка регистрации — {expected_error}")
    def check_register_error(self, response: Response, expected_error: str):
        data = self.validate_response_model(response, 400, ErrorResponse)
        assert data.error == expected_error, f"Ошибка не та: '{data.error}' != '{expected_error}'"

    @allure.step("Проверка: логин успешен")
    def check_login_success(self, response: Response):
        data = self.validate_response_model(response, 200, LoginResponse)
        assert data.token, "Токен пустой после логина"

    @allure.step("Проверка: ошибка логина — {expected_error}")
    def check_login_error(self, response: Response, expected_error: str):
        data = self.validate_response_model(response, 400, ErrorResponse)
        assert data.error == expected_error, f"Ошибка не та: '{data.error}' != '{expected_error}'"
