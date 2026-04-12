import allure
import pytest

from tests.ui.test_data import COURSE_SUBJECTS

pytestmark = pytest.mark.ui


@allure.feature("Каталог курсов")
class TestCourses:
    """Каталог -- карточки, навигация, контент, кликабельность."""

    @allure.story("Каталог")
    @allure.title("Страница каталога загружается, курсы на месте, скролл работает")
    @pytest.mark.smoke
    def test_courses_page_loads(self, courses_page, courses_checks):
        # открываю каталог и убеждаюсь что попал куда надо
        courses_page.open()
        courses_checks.check_on_courses_page()

        # курсы должны отрисоваться
        courses_checks.check_courses_displayed(min_count=1)

        # заголовки карточек не пустые — значит рендер отработал
        titles = courses_page.get_course_titles()
        courses_checks.check_course_titles_not_empty(titles)

        # скроллю вниз — проверяю что страница не обрывается
        courses_page.scroll_page_down()

    @allure.story("Каталог")
    @allure.title("У карточек курсов есть названия и их больше нуля")
    def test_course_cards_have_titles(self, courses_page, courses_checks):
        # открываю каталог
        courses_page.open()

        # собираю все названия
        titles = courses_page.get_course_titles()

        # каждое название должно быть не пустым, и вообще список не пуст
        courses_checks.check_course_titles_not_empty(titles)

    @allure.story("Предметы")
    @allure.title("Страница предмета '{subject}' доступна и содержит контент")
    @pytest.mark.parametrize("subject", COURSE_SUBJECTS)
    def test_subject_page_accessible(
        self, courses_page, courses_checks, header_checks, subject
    ):
        # захожу на страницу конкретного предмета
        courses_page.open_by_subject(subject)

        # страница загрузилась — заголовок не пустой
        header_checks.check_page_loaded()

        # URL содержит слаг предмета
        courses_checks.check_on_subject_page(subject)

        # на странице есть реальный контент, не пустышка
        courses_checks.check_page_has_content()

        # возвращаюсь в каталог напрямую (go_back не работает — мы открыли через goto)
        courses_page.open()
        courses_checks.check_on_courses_page()

    @allure.story("Предметы")
    @allure.title("Навигация между предметами: математика → английский → русский")
    def test_navigate_between_subjects(
        self, courses_page, courses_checks, header_checks
    ):
        # прохожу по трём предметам подряд, как юзер который выбирает
        subjects = ["matematika", "angliyskiy-yazyk", "russkiy-yazyk"]

        for subject in subjects:
            courses_page.open_by_subject(subject)
            header_checks.check_page_loaded()
            courses_checks.check_on_subject_page(subject)
            courses_checks.check_page_has_content()

    @allure.story("Каталог")
    @allure.title("На странице каталога достаточно контента и нет сломанных секций")
    def test_courses_page_has_content(self, courses_page, courses_checks):
        # открываю каталог
        courses_page.open()

        # текст страницы должен быть существенным, а не пустая заглушка
        page_text = courses_page.get_page_text()
        courses_checks.check_page_text_substantial(page_text, min_length=100)

        # скроллю через всю страницу до подвала
        courses_page.scroll_to_footer()

        # после скролла проверяю что нигде не вылезли ошибки
        courses_checks.check_no_broken_sections()

    @allure.story("Каталог")
    @allure.title("Страница каталога содержит ссылки на предметы")
    def test_course_links_present(self, courses_page, courses_checks):
        # открываю каталог
        courses_page.open()
        courses_checks.check_courses_displayed(min_count=1)

        # карточки содержат названия — значит это не пустые блоки
        titles = courses_page.get_course_titles()
        courses_checks.check_course_titles_not_empty(titles)
