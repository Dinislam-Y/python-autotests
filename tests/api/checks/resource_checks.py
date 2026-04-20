import allure
from requests import Response

from tests.api.checks.base_api_checks import BaseApiChecks
from tests.api.models import ResourceListResponse, SingleResourceResponse


class ResourceChecks(BaseApiChecks):
    """Проверки для /api/unknown — тут важна и параметризация, и контракт ответа."""

    @allure.step("Проверка: ресурс найден (id={resource_id})")
    def check_resource_found(self, response: Response, resource_id: int):
        resource = self.validate_response_model(response, 200, SingleResourceResponse)
        assert resource.data.id == resource_id, (
            f"id ресурса не совпадает: ожидал {resource_id}, получил {resource.data.id}"
        )
        assert resource.data.name.strip(), "name пустой — контракт ресурса сломан"

    @allure.step("Проверка: ресурс не найден")
    def check_resource_not_found(self, response: Response):
        self.check_empty_json_object(response, expected_status=404)

    @allure.step("Проверка: список ресурсов (page={expected_page})")
    def check_resource_list(self, response: Response, expected_page: int):
        data = self.validate_response_model(response, 200, ResourceListResponse)
        assert data.page == expected_page, f"Страница не та: ожидал {expected_page}, получил {data.page}"
        assert len(data.data) > 0, f"Страница {expected_page} пустая"
        assert all(item.name.strip() for item in data.data), "У одного из ресурсов пустое name"
