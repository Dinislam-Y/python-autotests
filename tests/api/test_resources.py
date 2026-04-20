import allure
import pytest

from tests.api.test_data import NON_EXISTING_USER_ID

pytestmark = pytest.mark.api


@allure.feature("Resources API")
class TestResources:
    """Ресурсы — тут показываю параметризацию, она часто нужна на собесах."""

    @allure.story("Получение ресурса")
    @allure.title("Ресурс #{resource_id} существует")
    @pytest.mark.parametrize("resource_id", [1, 2, 3], ids=["cerulean", "fuchsia_rose", "true_red"])
    def test_get_resource_by_id(self, api_client, resource_checks, resource_id):
        response = api_client.get(f"/api/unknown/{resource_id}")
        resource_checks.check_resource_found(response, resource_id)

    @allure.story("Получение ресурса")
    @allure.title("Несуществующий ресурс — 404")
    def test_resource_not_found(self, api_client, resource_checks):
        response = api_client.get(f"/api/unknown/{NON_EXISTING_USER_ID}")
        resource_checks.check_resource_not_found(response)

    @allure.story("Пагинация")
    @allure.title("Пагинация ресурсов — страница {page}")
    @pytest.mark.parametrize("page", [1, 2])
    def test_resources_list_pagination(self, api_client, resource_checks, page):
        response = api_client.get("/api/unknown", params={"page": page})
        resource_checks.check_resource_list(response, expected_page=page)
