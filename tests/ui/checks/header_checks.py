import allure
from playwright.sync_api import Page

from tests.ui.locators.header_locators import HeaderLocators


class HeaderChecks:
    """Проверки навигации — URL, загрузка страницы."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка: URL содержит '{expected_path}'")
    def check_navigated_to(self, expected_path: str):
        current = self.page.url
        assert expected_path in current, f"Ожидал '{expected_path}' в URL, а получил: {current}"

    @allure.step("Проверка: URL НЕ содержит '{unexpected_path}'")
    def check_not_on_page(self, unexpected_path: str):
        current = self.page.url
        assert unexpected_path not in current, f"Не ожидал '{unexpected_path}' в URL, а он там: {current}"

    @allure.step("Проверка: страница загрузилась")
    def check_page_loaded(self):
        title = self.page.title()
        assert title, "Заголовок страницы пустой — что-то не загрузилось"

    @allure.step("Проверка: заголовок страницы не пустой")
    def check_title_not_empty(self):
        # просто убеждаюсь что title есть — значит страница отрендерилась
        title = self.page.title()
        assert len(title.strip()) > 0, "Заголовок пустой или состоит из пробелов"

    @allure.step("Проверка: на странице есть контент (body не пустой)")
    def check_page_has_content(self):
        # проверяю что body не пустышка — хоть какой-то текст должен быть
        body_text = self.page.locator("body").first.inner_text()
        assert len(body_text.strip()) > 0, "Страница пустая — body без текста"

    @allure.step("Проверка: вернулись на главную")
    def check_returned_to_main(self):
        url = self.page.url
        # на главной URL заканчивается на домен или домен со слэшем
        # примеры: https://cms-dev.tochka-school.ru или https://cms-dev.tochka-school.ru/
        clean = url.rstrip("/")
        assert clean.endswith("tochka-school.ru"), f"Не на главной: {url}"

    @allure.step("Проверка: логотип виден")
    def check_logo_visible(self):
        logo = self.page.locator(HeaderLocators.LOGO).first
        assert logo.is_visible(), "Логотип не виден — шапка сломалась?"

    @allure.step("Проверка: URL изменился (не совпадает с '{previous_url}')")
    def check_url_changed(self, previous_url: str):
        # убеждаюсь что реально перешли куда-то, а не остались на месте
        current = self.page.url
        assert current != previous_url, f"URL не изменился, всё ещё: {current}"
