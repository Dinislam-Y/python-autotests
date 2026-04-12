import json
import logging

import allure
import requests

logger = logging.getLogger(__name__)


class ApiClient:
    """Обёртка над requests.Session — чтобы не таскать base_url в каждом тесте."""

    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url
        self.session = requests.Session()
        # reqres теперь за cloudflare, без ключа возвращает 403
        if api_key:
            self.session.headers["x-api-key"] = api_key

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _log_and_attach(self, method: str, url: str, response: requests.Response):
        """Логирую запрос + прикладываю ответ в allure, удобно при дебаге."""
        logger.info(f"{method} {url} -> {response.status_code}")
        try:
            body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        except ValueError:
            body = response.text or "(пустой ответ)"
        allure.attach(body=body, name=f"{method} {url}", attachment_type=allure.attachment_type.JSON)

    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        response = self.session.get(url, **kwargs)
        self._log_and_attach("GET", url, response)
        return response

    def post(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        response = self.session.post(url, **kwargs)
        self._log_and_attach("POST", url, response)
        return response

    def put(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        response = self.session.put(url, **kwargs)
        self._log_and_attach("PUT", url, response)
        return response

    def patch(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        response = self.session.patch(url, **kwargs)
        self._log_and_attach("PATCH", url, response)
        return response

    def delete(self, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        response = self.session.delete(url, **kwargs)
        self._log_and_attach("DELETE", url, response)
        return response
