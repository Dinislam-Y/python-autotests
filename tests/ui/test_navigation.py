import allure
import pytest

from tests.ui.test_data import (
    AGE_CATEGORIES,
    BLOG_URL,
    COURSES_URL,
    EGE_URL,
    MAIN_PAGE_TITLE_CONTAINS,
    OGE_URL,
    SUMMER_COURSES_URL,
)

pytestmark = pytest.mark.ui


@allure.feature("Навигация")
class TestNavigation:
    """Переходы между разделами сайта — многошаговые сценарии."""

    @allure.story("Главная страница")
    @allure.title("Главная: открытие, скролл вниз-вверх, баннер на месте")
    @pytest.mark.smoke
    def test_main_page_opens(self, main_page, main_page_checks, header_page):
        # открываю главную и проверяю заголовок
        main_page.open()
        main_page_checks.check_title_contains(MAIN_PAGE_TITLE_CONTAINS)

        # скроллю вниз — типа юзер листает страницу
        header_page.scroll_to_bottom()

        # возвращаюсь наверх — баннер должен остаться на месте
        header_page.scroll_to_top()
        main_page_checks.check_hero_banner_visible()
        main_page_checks.check_title_contains(MAIN_PAGE_TITLE_CONTAINS)

    @allure.story("Разделы")
    @allure.title("Раздел {url_path}: переход, контент, возврат на главную")
    @pytest.mark.parametrize("url_path", [
        COURSES_URL, SUMMER_COURSES_URL, BLOG_URL, OGE_URL, EGE_URL,
    ])
    def test_section_pages_accessible(self, main_page, header_page, header_checks, url_path):
        # открываю главную как стартовую точку
        main_page.open()

        # перехожу в раздел и проверяю что попал куда надо
        header_page.go_to_section(url_path)
        header_checks.check_navigated_to(url_path)
        header_checks.check_page_loaded()

        # убеждаюсь что заголовок не пустой — страница реально отрендерилась
        header_checks.check_title_not_empty()

        # контент должен быть — не заглушка
        header_checks.check_page_has_content()

        # возвращаюсь на главную через логотип и проверяю
        header_page.click_logo()
        header_checks.check_returned_to_main()

    @allure.story("Возрастные категории")
    @allure.title("Категория {category}: переход, контент, переход в другую категорию")
    @pytest.mark.parametrize("category,path", list(AGE_CATEGORIES.items()))
    def test_age_category_navigation(self, main_page, header_page, header_checks, category, path):
        # стартую с главной
        main_page.open()

        # перехожу в выбранную категорию
        header_page.go_to_section(path)
        header_checks.check_navigated_to(path)

        # страница не пустышка — есть контент
        header_checks.check_page_has_content()
        header_checks.check_title_not_empty()

        # перехожу в другую категорию чтобы убедиться что навигация работает по цепочке
        other_path = _pick_other_category(path)
        header_page.go_to_section(other_path)
        header_checks.check_navigated_to(other_path)
        header_checks.check_page_has_content()

    @allure.story("Логотип")
    @allure.title("Логотип: возврат на главную с раздела, повторный клик остаёмся")
    def test_logo_returns_to_main(self, main_page, header_page, header_checks):
        # ухожу со стартовой на курсы
        main_page.open()
        header_page.go_to_all_courses()
        header_checks.check_navigated_to(COURSES_URL)

        # кликаю логотип — должен вернуться на главную
        header_page.click_logo()
        header_checks.check_returned_to_main()

        # кликаю логотип ещё раз — должен остаться на главной
        header_page.click_logo()
        header_checks.check_returned_to_main()
        header_checks.check_logo_visible()

    @allure.story("Цепочка навигации")
    @allure.title("Последовательный обход 3 разделов без возврата на главную")
    def test_multiple_section_navigation(self, main_page, header_page, header_checks):
        # стартую с главной
        main_page.open()

        # прохожу по трём разделам подряд — не возвращаясь на главную
        sections = [COURSES_URL, BLOG_URL, OGE_URL]
        for section_url in sections:
            header_page.go_to_section(section_url)
            header_checks.check_navigated_to(section_url)
            header_checks.check_page_loaded()
            header_checks.check_page_has_content()

        # после обхода логотип должен быть на месте
        header_checks.check_logo_visible()

    @allure.story("Кнопка назад")
    @allure.title("Кнопка назад: переход вперёд, возврат, проверка URL")
    def test_back_button_works(self, main_page, header_page, header_checks):
        # открываю главную
        main_page.open()

        # ухожу на курсы
        header_page.go_to_section(COURSES_URL)
        header_checks.check_navigated_to(COURSES_URL)

        # потом на блог
        header_page.go_to_section(BLOG_URL)
        header_checks.check_navigated_to(BLOG_URL)

        # жму «назад» — должен вернуться на курсы
        header_page.go_back()
        header_checks.check_navigated_to(COURSES_URL)
        header_checks.check_not_on_page(BLOG_URL)

        # ещё раз «назад» — должен попасть на главную
        header_page.go_back()
        header_checks.check_returned_to_main()

    @allure.story("Цепочка навигации")
    @allure.title("Глубокая навигация: главная -> курсы -> категория -> обратно")
    def test_navigation_breadcrumbs_work(self, main_page, header_page, header_checks):
        # строю цепочку переходов: главная -> курсы -> категория
        main_page.open()
        header_checks.check_returned_to_main()

        # шаг 1 — ухожу на курсы
        header_page.go_to_section(COURSES_URL)
        header_checks.check_navigated_to(COURSES_URL)

        # шаг 2 — ухожу в возрастную категорию
        first_category = list(AGE_CATEGORIES.values())[0]
        header_page.go_to_section(first_category)
        header_checks.check_navigated_to(first_category)
        header_checks.check_page_has_content()

        # раскручиваю обратно через кнопку «назад»
        header_page.go_back()
        header_checks.check_navigated_to(COURSES_URL)

        header_page.go_back()
        header_checks.check_returned_to_main()


def _pick_other_category(current_path: str) -> str:
    """Выбираю другую категорию — просто беру первую, которая не совпадает."""
    for path in AGE_CATEGORIES.values():
        if path != current_path:
            return path
    # если вдруг одна категория (не бывает), вернём её же
    return current_path
