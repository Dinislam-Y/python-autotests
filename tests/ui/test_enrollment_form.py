import allure
import pytest

pytestmark = pytest.mark.ui


@allure.feature("Форма записи")
class TestEnrollmentForm:
    """Форма 'Подобрать занятия' — проверяем UI, не отправляем реально."""

    @allure.story("Отображение")
    @allure.title("Форма записи открывается из модалки")
    @pytest.mark.smoke
    def test_form_opens_from_modal(self, main_page, form_page, form_checks):
        # открываю главную, жму кнопку записи, проверяю модалку
        main_page.open()
        form_page.open_enrollment_modal()
        form_checks.check_form_visible()
        form_checks.check_submit_button_visible()

    @allure.story("Поля формы")
    @allure.title("Поле телефона видно и кликабельно")
    def test_phone_field_present(self, main_page, form_page, form_checks):
        main_page.open()
        form_page.open_enrollment_modal()
        form_checks.check_phone_field_present()
        form_page.click_phone_field()
        # после клика поле должно быть видимым — значит кликабельно
        form_checks.check_phone_field_present()

    @allure.story("Поля формы")
    @allure.title("Кнопка 'Записаться' видна")
    def test_submit_button_visible(self, main_page, form_page, form_checks):
        main_page.open()
        form_page.open_enrollment_modal()
        form_checks.check_submit_button_visible()

    @allure.story("Взаимодействие")
    @allure.title("Модалка закрывается по Escape и открывается повторно")
    def test_form_close_and_reopen(self, main_page, form_page, form_checks):
        # открыл → закрыл Escape → скрылась → снова открыл
        main_page.open()
        form_page.open_enrollment_modal()
        form_checks.check_form_visible()
        form_page.close_modal()
        form_checks.check_form_hidden()
        form_page.open_enrollment_modal()
        form_checks.check_form_visible()

    @allure.story("Взаимодействие")
    @allure.title("Ввод телефона в форму сохраняется")
    def test_phone_input_works(self, main_page, form_page, form_checks):
        # открываю модалку, вбиваю телефон, проверяю значение
        main_page.open()
        form_page.open_enrollment_modal()
        form_page.fill_phone("9991234567")
        form_checks.check_phone_has_value("999")
