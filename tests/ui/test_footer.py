import allure
import pytest

from tests.ui.test_data import BASE_URL, FOOTER_LICENSE_TEXT_CONTAINS

pytestmark = pytest.mark.ui


@allure.feature("Футер")
class TestFooter:
    """Футер -- соцсети, документы, лицензия."""

    @allure.story("Отображение")
    @allure.title("Футер виден после скролла + текст лицензии")
    @pytest.mark.smoke
    def test_footer_visible(self, main_page, footer_page, footer_checks):
        # открываю главную
        main_page.open()
        # скроллю до самого низа
        footer_page.scroll_to_footer()
        # футер виден
        footer_checks.check_footer_visible()
        # текст лицензии на месте
        footer_checks.check_footer_text_contains(FOOTER_LICENSE_TEXT_CONTAINS)

    @allure.story("Соцсети")
    @allure.title("Ссылки на соцсети >= 5 и у каждой есть href")
    def test_social_links_present(self, main_page, footer_page, footer_checks):
        # открываю главную
        main_page.open()
        # скроллю к подвалу
        footer_page.scroll_to_footer()
        # минимум 5 ссылок на соцсети
        footer_checks.check_social_links_count(expected=5)
        # каждая ссылка имеет непустой href
        footer_checks.check_social_links_have_href()

    @allure.story("Документы")
    @allure.title("Ссылки на документы >= 3")
    def test_documents_present(self, main_page, footer_page, footer_checks):
        # открываю главную
        main_page.open()
        # скроллю к подвалу
        footer_page.scroll_to_footer()
        # минимум 3 ссылки на документы
        footer_checks.check_documents_present(min_count=3)

    @allure.story("Лицензия")
    @allure.title("Текст и номер лицензии отображаются")
    def test_license_info(self, main_page, footer_page, footer_checks):
        # открываю главную
        main_page.open()
        # скроллю к подвалу
        footer_page.scroll_to_footer()
        # вижу слово "Лицензия"
        footer_checks.check_license_text_visible()
        # в тексте есть номер (цифры)
        footer_checks.check_license_number_present()

    @allure.story("Навигация")
    @allure.title("Футер на месте после перехода на /filter_courses")
    def test_footer_after_navigation(self, header_page, footer_page, footer_checks):
        # иду напрямую на страницу каталога
        header_page.go_to_section("/filter_courses")
        # скроллю к подвалу
        footer_page.scroll_to_footer()
        # футер виден и на этой странице тоже
        footer_checks.check_footer_visible()

    @allure.story("Соцсети")
    @allure.title("URL соцсетей содержат известные домены")
    def test_social_links_have_valid_urls(self, main_page, footer_page, footer_checks):
        # открываю главную
        main_page.open()
        # скроллю к подвалу
        footer_page.scroll_to_footer()
        # собираю все href
        hrefs = footer_page.get_social_link_hrefs()
        # каждый href должен содержать t.me / vk.com / youtube / tiktok / max.ru
        footer_checks.check_social_hrefs_contain_known_domains(hrefs)
