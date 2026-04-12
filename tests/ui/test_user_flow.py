import allure
import pytest

from tests.ui.test_data import BASE_URL, COURSES_URL, MAIN_PAGE_TITLE_CONTAINS, AGE_CATEGORIES

pytestmark = pytest.mark.ui


@allure.feature("User Flow")
class TestUserFlow:
    """Сквозные сценарии -- как реальный пользователь ходит по сайту."""

    @allure.story("Просмотр курсов")
    @allure.title("Главная -> каталог -> предмет -> назад на главную")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_browse_courses_flow(self, main_page, header_page, courses_page, header_checks, main_page_checks, courses_checks):
        # 1. открываю главную
        main_page.open()
        main_page_checks.check_title_contains(MAIN_PAGE_TITLE_CONTAINS)

        # 2. иду в каталог
        header_page.go_to_all_courses()
        courses_checks.check_on_courses_page()
        courses_checks.check_courses_displayed(min_count=1)

        # 3. открываю математику
        courses_page.open_by_subject("matematika")
        header_checks.check_page_loaded()

        # 4. возвращаюсь на главную через логотип
        header_page.click_logo()
        header_checks.check_returned_to_main()

    @allure.story("Запись на курс")
    @allure.title("Главная -> форма записи -> заполнение -> закрытие")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_enrollment_flow(self, main_page, form_page, form_checks, main_page_checks):
        # 1. открываю главную
        main_page.open()
        main_page_checks.check_hero_banner_visible()

        # 2. открываю форму записи
        form_page.open_enrollment_modal()
        form_checks.check_form_visible()

        # 3. ввожу телефон
        form_page.fill_phone("9991234567")

        # 4. закрываю без отправки
        form_page.close_modal()

    @allure.story("Полный обзор сайта")
    @allure.title("Главная -> скролл -> курсы -> блог -> главная")
    def test_full_site_tour(self, main_page, header_page, courses_page, footer_page, header_checks, main_page_checks, footer_checks):
        # 1. главная -- проверяю контент
        main_page.open()
        main_page_checks.check_hero_banner_visible()

        # 2. скроллю вниз -- футер на месте
        footer_page.scroll_to_footer()
        footer_checks.check_footer_visible()

        # 3. иду в каталог курсов
        header_page.go_to_all_courses()
        header_checks.check_navigated_to("/filter_courses")

        # 4. иду в блог
        header_page.go_to_section("/blog")
        header_checks.check_navigated_to("/blog")
        header_checks.check_page_loaded()

        # 5. возвращаюсь на главную
        header_page.click_logo()
        header_checks.check_returned_to_main()
