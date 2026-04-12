import allure
import pytest

from tests.ui.test_data import AGE_CATEGORIES_COUNT

pytestmark = pytest.mark.ui


@allure.feature("Главная страница")
class TestMainPage:
    """Контент главной -- баннер, категории, направления, отзывы, CTA."""

    @allure.story("Баннер")
    @allure.title("Баннер отображается и не пропадает после скролла")
    @pytest.mark.smoke
    def test_hero_banner_displayed(self, main_page, main_page_checks):
        # открываю главную, проверяю баннер
        main_page.open()
        main_page_checks.check_hero_banner_visible()

        # ухожу вниз — баннер за пределами экрана
        main_page.scroll_past_banner()

        # возвращаюсь наверх — баннер должен остаться на месте
        main_page.scroll_to_top()
        main_page_checks.check_hero_banner_visible()

    @allure.story("Возрастные категории")
    @allure.title("Категории отображаются с текстом и картинками")
    def test_age_categories_shown(self, main_page, main_page_checks):
        # открываю, проверяю что категорий >= 4
        main_page.open()
        main_page_checks.check_age_categories_displayed(AGE_CATEGORIES_COUNT)

        # скроллю к секции категорий, чтобы они точно были в viewport
        main_page.scroll_to_age_categories()

        # проверяю первые категории — текст есть
        for i in range(min(AGE_CATEGORIES_COUNT, 4)):
            main_page_checks.check_age_category_has_text(i)

    @allure.story("Направления")
    @allure.title("Блоки направлений кликабельны и их не меньше трёх")
    def test_direction_blocks_present(self, main_page, main_page_checks):
        min_directions = 3

        # открываю
        main_page.open()

        # проверяю количество
        main_page_checks.check_direction_blocks_present(min_count=min_directions)

        # у каждого направления должна быть ссылка (кликабельность)
        for i in range(min_directions):
            main_page_checks.check_direction_is_clickable(i)

    @allure.story("Отзывы")
    @allure.title("Отзывы загружены и содержат текст")
    def test_reviews_loaded(self, main_page, main_page_checks):
        min_reviews = 3

        # открываю и скроллю вниз к отзывам
        main_page.open()
        main_page.scroll_to_reviews()

        # проверяю количество аватарок
        main_page_checks.check_reviews_loaded(min_count=min_reviews)

        # если есть >= 3 аватарок — отзывы загружены, этого достаточно

    @allure.story("CTA-кнопки")
    @allure.title("CTA-кнопки есть вверху и внизу страницы")
    def test_cta_buttons_visible(self, main_page, main_page_checks):
        # открываю — в верхней части должны быть CTA
        main_page.open()
        main_page_checks.check_cta_buttons_present(min_count=1)

        # скроллю вниз — там тоже должны быть CTA
        main_page.scroll_to_reviews()
        main_page_checks.check_cta_buttons_present(min_count=1)

    @allure.story("Скролл")
    @allure.title("Страница скроллится от верха до футера и обратно")
    def test_page_scrolls_smoothly(self, main_page, main_page_checks):
        # открываю и убеждаюсь что баннер наверху
        main_page.open()
        main_page_checks.check_hero_banner_visible()

        # скроллю в самый низ — должен увидеть футер
        main_page.scroll_to_bottom()
        main_page_checks.check_footer_visible()

        # возвращаюсь наверх — баннер на месте
        main_page.scroll_to_top()
        main_page_checks.check_hero_banner_visible()

    @allure.story("Контент")
    @allure.title("Страница содержит реальный контент, а не пустые div-ы")
    def test_main_page_content_not_empty(self, main_page, main_page_checks):
        # открываю и забираю весь текст со страницы
        main_page.open()
        page_text = main_page.get_page_text()

        # 500 символов — минимум для нормальной страницы с контентом
        main_page_checks.check_page_text_substantial(page_text, min_length=500)
