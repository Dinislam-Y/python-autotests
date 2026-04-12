import allure
from playwright.sync_api import Page

from tests.ui.locators.footer_locators import FooterLocators
from tests.ui.pages.base_page import BasePage


class FooterPage(BasePage):
    """Футер — соцсети, документы, лицензия."""

    @allure.step("Скролл к футеру")
    def scroll_to_footer(self):
        # на сайте нет <footer>, скроллю в самый низ страницы
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)  # подождать подгрузку

    @allure.step("Подсчёт ссылок на соцсети")
    def get_social_links_count(self) -> int:
        return self.page.locator(FooterLocators.SOCIAL_LINKS).count()

    @allure.step("Подсчёт ссылок на документы")
    def get_document_links_count(self) -> int:
        return self.page.locator(FooterLocators.DOCUMENTS_LINKS).count()

    @allure.step("Получение текста футера")
    def get_footer_text(self) -> str:
        return self.page.locator(FooterLocators.FOOTER).first.text_content()

    @allure.step("Получение href всех ссылок на соцсети")
    def get_social_link_hrefs(self) -> list[str]:
        links = self.page.locator(FooterLocators.SOCIAL_LINKS)
        count = links.count()
        hrefs = []
        for i in range(count):
            href = links.nth(i).get_attribute("href")
            if href:
                hrefs.append(href)
        return hrefs
