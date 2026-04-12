import allure

from tests.ui.locators.courses_locators import CoursesLocators
from tests.ui.pages.base_page import BasePage
from tests.ui.test_data import BASE_URL


class CoursesPage(BasePage):
    """Каталог курсов — /filter_courses."""

    @allure.step("Открытие каталога курсов")
    def open(self):
        self.page.goto(f"{BASE_URL}/filter_courses", wait_until="networkidle")
        # ждём пока JS отрисует карточки курсов
        self.page.wait_for_timeout(2000)

    @allure.step("Открытие курса по предмету: {subject}")
    def open_by_subject(self, subject: str):
        self.page.goto(f"{BASE_URL}/filter_courses/{subject}", wait_until="networkidle")
        self.page.wait_for_timeout(2000)

    @allure.step("Подсчёт карточек курсов")
    def get_course_cards_count(self) -> int:
        return self.page.locator(CoursesLocators.COURSE_CARD).count()

    @allure.step("Получение названий курсов")
    def get_course_titles(self) -> list[str]:
        return self.page.locator(CoursesLocators.COURSE_TITLE).all_text_contents()

    @allure.step("Скролл вниз страницы каталога")
    def scroll_page_down(self):
        # прокручиваю страницу вниз чтобы подгрузить контент
        self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    @allure.step("Получение текста страницы")
    def get_page_text(self) -> str:
        return self.page.locator(CoursesLocators.PAGE_BODY).inner_text()

    @allure.step("Клик по первой карточке курса")
    def click_first_course_card(self):
        # кликаю по первой попавшейся карточке
        self.page.locator(CoursesLocators.COURSE_CARD).first.click()
        self.page.wait_for_timeout(2000)

    @allure.step("Возврат назад через браузер")
    def go_back(self):
        self.page.go_back(wait_until="networkidle")
        self.page.wait_for_timeout(1000)

    @allure.step("Скролл к подвалу страницы")
    def scroll_to_footer(self):
        # пробуем доскроллить до footer, если нету — просто до конца страницы
        footer = self.page.locator(CoursesLocators.FOOTER)
        if footer.count() > 0:
            footer.first.scroll_into_view_if_needed()
        else:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
