import allure
from playwright.sync_api import Page


class BasePage:
    """Базовый класс — общие методы для всех страниц."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открытие страницы: {url}")
    def open(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    @allure.step("Скролл к элементу: {selector}")
    def scroll_to(self, selector: str):
        self.page.locator(selector).first.scroll_into_view_if_needed()
