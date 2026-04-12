import allure
from playwright.sync_api import Page

from tests.ui.locators.courses_locators import CoursesLocators


class CoursesChecks:
    """Проверки каталога курсов."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка: курсы отображаются (минимум {min_count})")
    def check_courses_displayed(self, min_count: int = 1):
        actual = self.page.locator(CoursesLocators.COURSE_CARD).count()
        assert actual >= min_count, f"Курсов меньше {min_count}: нашёл {actual}"

    @allure.step("Проверка: у каждого курса есть название")
    def check_course_titles_not_empty(self, titles: list[str]):
        assert len(titles) > 0, "Список названий пуст, ни одного курса не нашлось"
        for i, title in enumerate(titles):
            assert title.strip(), f"Курс #{i} без названия"

    @allure.step("Проверка: на странице каталога курсов")
    def check_on_courses_page(self):
        assert "/filter_courses" in self.page.url, f"Не на странице курсов: {self.page.url}"

    @allure.step("Проверка: на странице предмета '{subject}'")
    def check_on_subject_page(self, subject: str):
        # в URL должен быть слаг предмета
        assert subject in self.page.url, (
            f"Ожидал '{subject}' в URL, получил: {self.page.url}"
        )

    @allure.step("Проверка: страница содержит контент по предмету")
    def check_page_has_content(self):
        # на странице предмета должен быть хоть какой-то текст, не пустышка
        body_text = self.page.locator(CoursesLocators.PAGE_BODY).inner_text()
        assert len(body_text.strip()) > 50, (
            f"На странице слишком мало текста ({len(body_text.strip())} символов)"
        )

    @allure.step("Проверка: текст страницы существенный (больше {min_length} символов)")
    def check_page_text_substantial(self, text: str, min_length: int = 100):
        assert len(text.strip()) > min_length, (
            f"Текст страницы слишком короткий: {len(text.strip())} символов, ожидал > {min_length}"
        )

    @allure.step("Проверка: нет сломанных секций на странице")
    def check_no_broken_sections(self):
        # типичные признаки что что-то сломалось — ошибки в тексте страницы
        body_text = self.page.locator(CoursesLocators.PAGE_BODY).inner_text().lower()
        # "500" убрал — часто встречается в ценах. "404" тоже может быть в тексте
        broken_markers = ["not found", "ошибка сервера", "internal server error", "page not found"]
        for marker in broken_markers:
            assert marker not in body_text, (
                f"Нашёл признак сломанной секции: '{marker}' в тексте страницы"
            )

    @allure.step("Проверка: перешли на другую страницу (не 404)")
    def check_navigated_not_404(self, original_url: str):
        current_url = self.page.url
        body_text = self.page.locator(CoursesLocators.PAGE_BODY).inner_text().lower()
        # не должны остаться на той же странице и не должно быть 404
        assert "404" not in body_text, "Попали на страницу 404"
        assert "not found" not in body_text, "Попали на страницу Not Found"

    @allure.step("Проверка: вернулись в каталог курсов")
    def check_returned_to_catalog(self):
        assert "/filter_courses" in self.page.url, (
            f"Не вернулись в каталог: {self.page.url}"
        )
