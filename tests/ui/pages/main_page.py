import allure
from playwright.sync_api import Page

from tests.ui.locators.main_page_locators import MainPageLocators
from tests.ui.pages.base_page import BasePage
from tests.ui.test_data import BASE_URL


class MainPage(BasePage):
    """Главная страница — баннер, категории, направления, отзывы."""

    @allure.step("Открытие главной страницы")
    def open(self):
        super().open(BASE_URL)

    # --- подсчёты ---

    @allure.step("Подсчёт карточек возрастных категорий")
    def get_age_category_count(self) -> int:
        return self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).count()

    @allure.step("Подсчёт блоков направлений")
    def get_direction_blocks_count(self) -> int:
        return self.page.locator(MainPageLocators.DIRECTION_BLOCKS).count()

    @allure.step("Подсчёт отзывов")
    def get_reviews_count(self) -> int:
        return self.page.locator(MainPageLocators.REVIEW_ITEMS).count()

    @allure.step("Подсчёт CTA-кнопок")
    def get_cta_buttons_count(self) -> int:
        return self.page.locator(MainPageLocators.CTA_BUTTONS).count()

    # --- скроллы ---

    @allure.step("Скролл к баннеру (вверх страницы)")
    def scroll_to_top(self):
        # просто крутим наверх через JS — надёжнее, чем scroll_into_view
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(300)

    @allure.step("Скролл мимо баннера вниз")
    def scroll_past_banner(self):
        # проматываю на 800px — достаточно, чтобы баннер уехал из вьюпорта
        self.page.evaluate("window.scrollBy(0, 800)")
        self.page.wait_for_timeout(300)

    @allure.step("Скролл к секции возрастных категорий")
    def scroll_to_age_categories(self):
        self.scroll_to(MainPageLocators.AGE_CATEGORY_SECTION)

    @allure.step("Скролл к направлениям")
    def scroll_to_directions(self):
        self.page.locator(MainPageLocators.DIRECTION_BLOCKS).first.scroll_into_view_if_needed()

    @allure.step("Скролл к отзывам")
    def scroll_to_reviews(self):
        self.scroll_to(MainPageLocators.REVIEWS_SECTION)

    @allure.step("Скролл в самый низ страницы")
    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(500)

    # --- данные со страницы ---

    @allure.step("Получение текста всей страницы")
    def get_page_text(self) -> str:
        return self.page.locator(MainPageLocators.PAGE_BODY).inner_text()

    @allure.step("Получение текста категории #{index}")
    def get_age_category_text(self, index: int) -> str:
        return self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).nth(index).inner_text()

    @allure.step("Проверка наличия картинки в категории #{index}")
    def age_category_has_image(self, index: int) -> bool:
        card = self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).nth(index)
        return card.locator("img").count() > 0

    @allure.step("Получение href направления #{index}")
    def get_direction_href(self, index: int) -> str:
        return self.page.locator(MainPageLocators.DIRECTION_BLOCKS).nth(index).get_attribute("href") or ""

    @allure.step("Получение текста отзыва #{index}")
    def get_review_text(self, index: int) -> str:
        # берём текст ближайшей ссылки "Читать весь отзыв"
        links = self.page.locator(MainPageLocators.REVIEW_TEXT_LINKS)
        if links.count() > index:
            return links.nth(index).inner_text()
        return ""
