import allure
from playwright.sync_api import Page

from tests.ui.locators.main_page_locators import MainPageLocators


class MainPageChecks:
    """Проверки главной страницы."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка: баннер отображается")
    def check_hero_banner_visible(self):
        banner = self.page.locator(MainPageLocators.HERO_BANNER).first
        assert banner.is_visible(), "Баннер не виден на главной"

    @allure.step("Проверка: {expected_count} возрастных категорий")
    def check_age_categories_displayed(self, expected_count: int):
        actual = self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).count()
        # на сайте карточки дублируются для desktop/mobile, поэтому >= а не ==
        assert actual >= expected_count, f"Категорий меньше {expected_count}: нашёл {actual}"

    @allure.step("Проверка: категория #{index} содержит текст")
    def check_age_category_has_text(self, index: int):
        text = self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).nth(index).inner_text()
        assert len(text.strip()) > 0, f"Категория #{index} пустая — текста нет"

    @allure.step("Проверка: категория #{index} содержит картинку")
    def check_age_category_has_image(self, index: int):
        card = self.page.locator(MainPageLocators.AGE_CATEGORY_CARDS).nth(index)
        img_count = card.locator("img").count()
        assert img_count > 0, f"Категория #{index} без картинки"

    @allure.step("Проверка: блоки направлений есть на странице")
    def check_direction_blocks_present(self, min_count: int = 1):
        actual = self.page.locator(MainPageLocators.DIRECTION_BLOCKS).count()
        assert actual >= min_count, f"Направлений меньше {min_count}: нашёл {actual}"

    @allure.step("Проверка: направление #{index} кликабельно (есть href)")
    def check_direction_is_clickable(self, index: int):
        href = self.page.locator(MainPageLocators.DIRECTION_BLOCKS).nth(index).get_attribute("href")
        assert href and len(href) > 0, f"Направление #{index} не имеет ссылки"

    @allure.step("Проверка: отзывы загрузились (минимум {min_count})")
    def check_reviews_loaded(self, min_count: int = 1):
        actual = self.page.locator(MainPageLocators.REVIEW_ITEMS).count()
        assert actual >= min_count, f"Отзывов меньше {min_count}: нашёл {actual}"

    @allure.step("Проверка: у отзывов есть текстовый контент")
    def check_reviews_have_text(self):
        links = self.page.locator(MainPageLocators.REVIEW_TEXT_LINKS)
        count = links.count()
        assert count > 0, "Ссылок 'Читать весь отзыв' не найдено"
        for i in range(min(count, 3)):
            text = links.nth(i).inner_text()
            assert len(text.strip()) > 0, f"Ссылка отзыва #{i} пустая"

    @allure.step("Проверка: CTA-кнопки есть (минимум {min_count})")
    def check_cta_buttons_present(self, min_count: int = 1):
        actual = self.page.locator(MainPageLocators.CTA_BUTTONS).count()
        assert actual >= min_count, f"CTA-кнопок меньше {min_count}: нашёл {actual}"

    @allure.step("Проверка: футер отображается")
    def check_footer_visible(self):
        footer = self.page.locator(MainPageLocators.FOOTER_AREA).first
        assert footer.is_visible(), "Футер (текст лицензии) не найден внизу страницы"

    @allure.step("Проверка: текст страницы не пустой (минимум {min_length} символов)")
    def check_page_text_substantial(self, text: str, min_length: int = 500):
        assert len(text) >= min_length, (
            f"Страница подозрительно пустая: {len(text)} символов (ожидал >= {min_length})"
        )

    @allure.step("Проверка: заголовок содержит '{text}'")
    def check_title_contains(self, text: str):
        title = self.page.title()
        assert text.lower() in title.lower(), f"'{text}' не найден в заголовке: '{title}'"
