import allure
from requests import Response

from tests.api.checks.base_api_checks import BaseApiChecks
from tests.api.models import CreateUserResponse, SingleUserResponse, UpdateUserResponse, UserListResponse


class UserChecks(BaseApiChecks):
    """Проверки для /api/users — статусы, структура, значения полей."""

    @allure.step("Проверка: пользователь найден (id={user_id})")
    def check_user_found(self, response: Response, user_id: int):
        user = self.validate_response_model(response, 200, SingleUserResponse)
        assert user.data.id == user_id, f"id не совпадает: ожидал {user_id}, получил {user.data.id}"

    @allure.step("Проверка: список пользователей (page={expected_page})")
    def check_user_list(self, response: Response, expected_page: int):
        data = self.validate_response_model(response, 200, UserListResponse)
        assert data.page == expected_page, f"Страница не та: ожидал {expected_page}, получил {data.page}"
        assert len(data.data) > 0, "Список пользователей пустой"

    @allure.step("Проверка: пользователь не найден")
    def check_user_not_found(self, response: Response):
        self.check_empty_json_object(response, expected_status=404)

    @allure.step("Проверка: пользователь создан")
    def check_user_created(self, response: Response, name: str, job: str):
        user = self.validate_response_model(response, 201, CreateUserResponse)
        assert user.name == name, f"Имя не совпадает: {user.name} != {name}"
        assert user.job == job, f"Должность не совпадает: {user.job} != {job}"
        assert user.id, "id пустой — reqres должен вернуть строковый id"
        assert user.createdAt, "createdAt пустой — контракт создания пользователя сломан"

    @allure.step("Проверка: пользователь обновлён")
    def check_user_updated(self, response: Response, job: str):
        data = self.validate_response_model(response, 200, UpdateUserResponse)
        assert data.job == job, f"Должность не обновилась: {data.job} != {job}"
        assert data.updatedAt, "updatedAt пустой — контракт обновления пользователя сломан"

    @allure.step("Проверка: пользователь удалён")
    def check_user_deleted(self, response: Response):
        # reqres отдаёт 204 без тела — это тоже часть контракта
        self.check_no_content_response(response, expected_status=204)
