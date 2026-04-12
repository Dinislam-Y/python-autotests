import allure
from playwright.sync_api import Page

from tests.ui.locators.form_locators import FormLocators


class FormChecks:
    """Проверки формы записи."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка: форма записи видна")
    def check_form_visible(self):
        form = self.page.locator(FormLocators.FORM_CONTAINER).first
        assert form.is_visible(), "Форма записи не отображается"

    @allure.step("Проверка: форма записи скрыта")
    def check_form_hidden(self):
        form = self.page.locator(FormLocators.FORM_CONTAINER).first
        assert not form.is_visible(), "Форма записи всё ещё видна, хотя должна быть скрыта"

    @allure.step("Проверка: поле телефона на месте")
    def check_phone_field_present(self):
        phone = self.page.locator(FormLocators.PHONE_INPUT).first
        assert phone.is_visible(), "Поле телефона не найдено"

    @allure.step("Проверка: поле телефона в фокусе")
    def check_phone_field_focused(self):
        # после клика по полю оно должно быть активным
        phone = self.page.locator(FormLocators.PHONE_INPUT).first
        assert phone.is_focused(), "Поле телефона не получило фокус"

    @allure.step("Проверка: кнопка 'Записаться' видна")
    def check_submit_button_visible(self):
        btn = self.page.locator(FormLocators.SUBMIT_BUTTON).first
        assert btn.is_visible(), "Кнопка 'Записаться' не видна"

    @allure.step("Проверка: кнопка 'Записаться' доступна (enabled)")
    def check_submit_button_enabled(self):
        btn = self.page.locator(FormLocators.SUBMIT_BUTTON).first
        assert btn.is_enabled(), "Кнопка 'Записаться' задизейблена"

    @allure.step("Проверка: все основные поля формы на месте")
    def check_all_fields_present(self):
        # селект класса, телефон, чекбокс, кнопка — полный набор
        select = self.page.locator(FormLocators.CLASS_SELECT).first
        phone = self.page.locator(FormLocators.PHONE_INPUT).first
        checkbox = self.page.locator(FormLocators.CONSENT_CHECKBOX).first
        btn = self.page.locator(FormLocators.SUBMIT_BUTTON).first
        assert select.is_visible(), "Селект класса не отображается"
        assert phone.is_visible(), "Поле телефона не отображается"
        assert checkbox.is_visible(), "Чекбокс согласия не отображается"
        assert btn.is_visible(), "Кнопка 'Записаться' не отображается"

    @allure.step("Проверка: чекбокс согласия не отмечен по умолчанию")
    def check_consent_unchecked(self):
        checkbox = self.page.locator(FormLocators.CONSENT_CHECKBOX).first
        assert not checkbox.is_checked(), "Чекбокс уже отмечен, а не должен быть"

    @allure.step("Проверка: чекбокс согласия отмечен")
    def check_consent_checked(self):
        checkbox = self.page.locator(FormLocators.CONSENT_CHECKBOX).first
        assert checkbox.is_checked(), "Чекбокс должен быть отмечен, но он не отмечен"

    @allure.step("Проверка: селект класса существует")
    def check_class_select_present(self):
        select = self.page.locator(FormLocators.CLASS_SELECT).first
        assert select.is_visible(), "Селект класса не найден"

    @allure.step("Проверка: в селекте есть опции ({min_count}+)")
    def check_class_select_has_options(self, min_count: int = 1):
        options = self.page.locator(FormLocators.CLASS_SELECT_OPTIONS)
        count = options.count()
        assert count >= min_count, (
            f"Ожидали минимум {min_count} опций в селекте класса, нашли {count}"
        )

    @allure.step("Проверка: телефон заполнен значением")
    def check_phone_has_value(self, expected_substring: str):
        phone = self.page.locator(FormLocators.PHONE_INPUT).first
        value = phone.input_value()
        assert expected_substring in value, (
            f"В поле телефона ожидали подстроку '{expected_substring}', а там '{value}'"
        )

    @allure.step("Проверка: в селекте класса выбрано значение")
    def check_class_has_value(self):
        select = self.page.locator(FormLocators.CLASS_SELECT).first
        value = select.input_value()
        assert value, "В селекте класса ничего не выбрано (пустое значение)"
