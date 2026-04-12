import allure
from playwright.sync_api import Page

from tests.ui.locators.header_locators import HeaderLocators
from tests.ui.pages.base_page import BasePage


class HeaderPage(BasePage):
    """Шапка сайта — навигация между разделами."""

    @allure.step("Клик по логотипу")
    def click_logo(self):
        self.page.locator(HeaderLocators.LOGO).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Переход: Все курсы")
    def go_to_all_courses(self):
        self.page.locator(HeaderLocators.NAV_ALL_COURSES).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Переход: Летние курсы")
    def go_to_summer_courses(self):
        self.page.locator(HeaderLocators.NAV_SUMMER_COURSES).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Переход: Блог")
    def go_to_blog(self):
        self.page.locator(HeaderLocators.NAV_BLOG).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Переход по URL: {path}")
    def go_to_section(self, path: str):
        # иду напрямую по URL — надёжнее чем искать ссылку в меню
        from tests.ui.test_data import BASE_URL
        self.page.goto(f"{BASE_URL}{path}", wait_until="domcontentloaded")

    @allure.step("Скролл в самый низ страницы")
    def scroll_to_bottom(self):
        # пуляю скролл вниз до упора
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(500)

    @allure.step("Скролл в самый верх страницы")
    def scroll_to_top(self):
        # обратно наверх
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(500)

    @allure.step("Назад через историю браузера")
    def go_back(self):
        # жму «назад» как обычный юзер
        self.page.go_back(wait_until="domcontentloaded")
