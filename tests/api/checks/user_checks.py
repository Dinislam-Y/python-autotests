import allure
from requests import Response

from tests.api.models import CreateUserResponse, SingleUserResponse, UpdateUserResponse, UserListResponse


class UserChecks:
    """Проверки для /api/users — статусы, структура, значения полей."""

    @allure.step("Проверка: пользователь найден (id={user_id})")
    def check_user_found(self, response: Response, user_id: int):
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        user = SingleUserResponse.model_validate(response.json())
        assert user.data.id == user_id, f"id не совпадает: ожидал {user_id}, получил {user.data.id}"

    @allure.step("Проверка: список пользователей (page={expected_page})")
    def check_user_list(self, response: Response, expected_page: int):
        assert response.status_code == 200
        data = UserListResponse.model_validate(response.json())
        assert data.page == expected_page, f"Страница не та: ожидал {expected_page}, получил {data.page}"
        assert len(data.data) > 0, "Список пользователей пустой"

    @allure.step("Проверка: пользователь не найден")
    def check_user_not_found(self, response: Response):
        assert response.status_code == 404, f"Ожидал 404, получил {response.status_code}"

    @allure.step("Проверка: пользователь создан")
    def check_user_created(self, response: Response, name: str, job: str):
        assert response.status_code == 201, f"Ожидал 201, получил {response.status_code}"
        user = CreateUserResponse.model_validate(response.json())
        assert user.name == name, f"Имя не совпадает: {user.name} != {name}"
        assert user.job == job, f"Должность не совпадает: {user.job} != {job}"
        assert user.id, "id пустой — reqres должен вернуть строковый id"

    @allure.step("Проверка: пользователь обновлён")
    def check_user_updated(self, response: Response, job: str):
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        data = UpdateUserResponse.model_validate(response.json())
        assert data.job == job, f"Должность не обновилась: {data.job} != {job}"

    @allure.step("Проверка: пользователь удалён")
    def check_user_deleted(self, response: Response):
        # reqres отдаёт 204 без тела — тут только статус проверяем
        assert response.status_code == 204, f"Ожидал 204, получил {response.status_code}"
