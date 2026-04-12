import allure
from playwright.sync_api import Page

from tests.ui.locators.form_locators import FormLocators
from tests.ui.pages.base_page import BasePage


class FormPage(BasePage):
    """Форма записи на занятия — заполнение, валидация."""

    @allure.step("Открытие модалки с формой записи")
    def open_enrollment_modal(self):
        # форма живёт в модалке, сначала надо её открыть
        self.page.locator(FormLocators.OPEN_MODAL_BUTTON).first.click()
        self.page.locator(FormLocators.FORM_CONTAINER).first.wait_for(state="visible")

    @allure.step("Выбор класса: {value}")
    def select_class(self, value: str):
        self.page.locator(FormLocators.CLASS_SELECT).first.select_option(label=value)

    @allure.step("Ввод телефона: {phone}")
    def fill_phone(self, phone: str):
        field = self.page.locator(FormLocators.PHONE_INPUT).first
        field.click()
        field.fill(phone)

    @allure.step("Клик: согласие на обработку данных")
    def check_consent(self):
        self.page.locator(FormLocators.CONSENT_CHECKBOX).first.check()

    @allure.step("Снятие галки: согласие на обработку данных")
    def uncheck_consent(self):
        self.page.locator(FormLocators.CONSENT_CHECKBOX).first.uncheck()

    @allure.step("Клик: Записаться")
    def submit(self):
        self.page.locator(FormLocators.SUBMIT_BUTTON).first.click()

    @allure.step("Клик по полю телефона (фокус)")
    def click_phone_field(self):
        self.page.locator(FormLocators.PHONE_INPUT).first.click()

    @allure.step("Закрытие модалки (Escape)")
    def close_modal(self):
        # жмём Escape — универсальный способ закрыть модалку
        self.page.keyboard.press("Escape")
        # даём модалке время на анимацию закрытия
        self.page.wait_for_timeout(500)

    def is_form_visible(self) -> bool:
        return self.page.locator(FormLocators.FORM_CONTAINER).first.is_visible()

    def is_consent_checked(self) -> bool:
        return self.page.locator(FormLocators.CONSENT_CHECKBOX).first.is_checked()

    def get_phone_value(self) -> str:
        return self.page.locator(FormLocators.PHONE_INPUT).first.input_value()

    def get_class_options_count(self) -> int:
        return self.page.locator(FormLocators.CLASS_SELECT_OPTIONS).count()

    def get_first_class_option_text(self) -> str:
        return self.page.locator(FormLocators.CLASS_SELECT_OPTIONS).first.inner_text()

    def get_selected_class_value(self) -> str:
        return self.page.locator(FormLocators.CLASS_SELECT).first.input_value()
