import allure
from playwright.sync_api import Page

from tests.ui.locators.footer_locators import FooterLocators


class FooterChecks:
    """Проверки футера."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка: футер виден")
    def check_footer_visible(self):
        assert self.page.locator(FooterLocators.FOOTER).first.is_visible(), "Футер не виден"

    @allure.step("Проверка: соцсети присутствуют (минимум {expected})")
    def check_social_links_count(self, expected: int):
        # ссылки на соцсети дублируются в хедере и футере, считаем общее кол-во
        actual = self.page.locator(FooterLocators.SOCIAL_LINKS).count()
        assert actual >= expected, f"Соцсетей меньше {expected}: нашёл {actual}"

    @allure.step("Проверка: документы есть (минимум {min_count})")
    def check_documents_present(self, min_count: int = 1):
        actual = self.page.locator(FooterLocators.DOCUMENTS_LINKS).count()
        assert actual >= min_count, f"Документов меньше {min_count}: нашёл {actual}"

    @allure.step("Проверка: текст футера содержит '{text}'")
    def check_footer_text_contains(self, text: str):
        # на сайте нет <footer>, ищем текст лицензии по отдельному локатору
        license_el = self.page.locator(FooterLocators.LICENSE_TEXT).first
        assert license_el.is_visible(), f"'{text}' не найден в футере"

    @allure.step("Проверка: ссылки на соцсети имеют непустой href")
    def check_social_links_have_href(self):
        links = self.page.locator(FooterLocators.SOCIAL_LINKS)
        count = links.count()
        assert count > 0, "Нет ни одной ссылки на соцсети"
        for i in range(count):
            href = links.nth(i).get_attribute("href")
            assert href and href.strip(), f"Ссылка на соцсеть #{i} без href"

    @allure.step("Проверка: текст лицензии виден")
    def check_license_text_visible(self):
        license_el = self.page.locator(FooterLocators.LICENSE_TEXT).first
        assert license_el.is_visible(), "Текст лицензии не виден"

    @allure.step("Проверка: информация о лицензии присутствует")
    def check_license_number_present(self):
        # на сайте текст "Наша лицензия" или "Лицензия №..." — проверяем что элемент виден
        license_el = self.page.locator(FooterLocators.LICENSE_TEXT).first
        assert license_el.is_visible(), "Информация о лицензии не найдена"

    @allure.step("Проверка: URL соцсетей содержат известные домены")
    def check_social_hrefs_contain_known_domains(self, hrefs: list[str]):
        known_domains = ("t.me", "vk.com", "youtube", "tiktok", "max.ru")
        for href in hrefs:
            matches = any(domain in href for domain in known_domains)
            assert matches, f"Ссылка '{href}' не содержит ни один из доменов: {known_domains}"
