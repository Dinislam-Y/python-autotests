from typing import TypeVar

import allure
from pydantic import BaseModel
from requests import Response

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseApiChecks:
    """Базовые контрактные проверки для JSON API."""

    @allure.step("Проверка контракта: JSON-ответ со статусом {expected_status}")
    def check_json_response(self, response: Response, expected_status: int) -> dict:
        assert response.status_code == expected_status, f"Ожидал {expected_status}, получил {response.status_code}"
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower(), (
            f"Ожидал JSON content-type, получил: '{content_type or 'пусто'}'"
        )
        return response.json()

    @allure.step("Проверка контракта: ответ соответствует схеме {model}")
    def validate_response_model(self, response: Response, expected_status: int, model: type[ModelT]) -> ModelT:
        payload = self.check_json_response(response, expected_status)
        return model.model_validate(payload)

    @allure.step("Проверка контракта: 404 возвращает пустой JSON")
    def check_empty_json_object(self, response: Response, expected_status: int = 404):
        payload = self.check_json_response(response, expected_status)
        assert payload == {}, f"Ожидал пустой JSON {{}} для {expected_status}, получил: {payload}"

    @allure.step("Проверка контракта: пустое тело со статусом {expected_status}")
    def check_no_content_response(self, response: Response, expected_status: int = 204):
        assert response.status_code == expected_status, f"Ожидал {expected_status}, получил {response.status_code}"
        assert not response.content, f"Ожидал пустое тело ответа, получил: {response.text!r}"
