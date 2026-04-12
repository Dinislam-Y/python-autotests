import allure
from requests import Response

from tests.api.models import ErrorResponse, LoginResponse, RegisterResponse


class AuthChecks:
    """Проверки для /api/register и /api/login."""

    @allure.step("Проверка: регистрация успешна")
    def check_register_success(self, response: Response):
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        data = RegisterResponse.model_validate(response.json())
        assert data.token, "Токен пустой после регистрации"
        assert data.id, "id пустой после регистрации"

    @allure.step("Проверка: ошибка регистрации — {expected_error}")
    def check_register_error(self, response: Response, expected_error: str):
        assert response.status_code == 400, f"Ожидал 400, получил {response.status_code}"
        data = ErrorResponse.model_validate(response.json())
        assert data.error == expected_error, f"Ошибка не та: '{data.error}' != '{expected_error}'"

    @allure.step("Проверка: логин успешен")
    def check_login_success(self, response: Response):
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        data = LoginResponse.model_validate(response.json())
        assert data.token, "Токен пустой после логина"

    @allure.step("Проверка: ошибка логина — {expected_error}")
    def check_login_error(self, response: Response, expected_error: str):
        assert response.status_code == 400, f"Ожидал 400, получил {response.status_code}"
        data = ErrorResponse.model_validate(response.json())
        assert data.error == expected_error, f"Ошибка не та: '{data.error}' != '{expected_error}'"
