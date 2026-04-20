import allure
import pytest

from tests.api.test_data import (
    CREATE_USER_JOB,
    CREATE_USER_NAME,
    EXISTING_USER_ID,
    NON_EXISTING_USER_ID,
    UPDATE_USER_JOB,
)

pytestmark = pytest.mark.api


@allure.feature("Users API")
class TestUsers:
    """CRUD тесты для /api/users — основа любого API-тестирования."""

    @allure.story("Получение пользователя")
    @allure.title("Получить существующего пользователя по id")
    def test_get_single_user(self, api_client, user_checks):
        response = api_client.get(f"/api/users/{EXISTING_USER_ID}")
        user_checks.check_user_found(response, EXISTING_USER_ID)

    @allure.story("Получение пользователя")
    @allure.title("Получить список пользователей (page=2)")
    def test_get_users_list(self, api_client, user_checks):
        response = api_client.get("/api/users", params={"page": 2})
        user_checks.check_user_list(response, expected_page=2)

    @allure.story("Получение пользователя")
    @allure.title("Пользователь не найден — 404")
    def test_user_not_found(self, api_client, user_checks):
        response = api_client.get(f"/api/users/{NON_EXISTING_USER_ID}")
        user_checks.check_user_not_found(response)

    @allure.story("Создание пользователя")
    @allure.title("Создать пользователя с именем и должностью")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api_client, user_checks):
        response = api_client.post("/api/users", json={"name": CREATE_USER_NAME, "job": CREATE_USER_JOB})
        user_checks.check_user_created(response, CREATE_USER_NAME, CREATE_USER_JOB)

    @allure.story("Обновление пользователя")
    @allure.title("Обновить пользователя через PUT")
    def test_update_user_put(self, api_client, user_checks):
        response = api_client.put(
            f"/api/users/{EXISTING_USER_ID}",
            json={"name": CREATE_USER_NAME, "job": UPDATE_USER_JOB},
        )
        user_checks.check_user_updated(response, UPDATE_USER_JOB)

    @allure.story("Обновление пользователя")
    @allure.title("Частичное обновление через PATCH")
    def test_update_user_patch(self, api_client, user_checks):
        response = api_client.patch(f"/api/users/{EXISTING_USER_ID}", json={"job": UPDATE_USER_JOB})
        user_checks.check_user_updated(response, UPDATE_USER_JOB)

    @allure.story("Удаление пользователя")
    @allure.title("Удалить пользователя — 204")
    def test_delete_user(self, api_client, user_checks):
        response = api_client.delete(f"/api/users/{EXISTING_USER_ID}")
        user_checks.check_user_deleted(response)
