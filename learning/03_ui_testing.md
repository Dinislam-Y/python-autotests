# UI-тестирование — Playwright Python

> От Flutter finders к CSS-локаторам. От `testWidgets` к `pytest`.
> Перед этим файлом прочитай [01_python_language.md](01_python_language.md) и [02_api_testing.md](02_api_testing.md)

---
---

## 1. Playwright — установка и основы

### Что это
Playwright — фреймворк для автоматизации браузеров. Один API для Chromium, Firefox, WebKit. Создан Microsoft, пришёл на замену Selenium.

### Установка

```bash
pip install playwright pytest-playwright
playwright install                        # скачивает браузеры (~400 МБ)
```

### Первый тест

```python
import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
```

`page` — фикстура от `pytest-playwright`, создаётся автоматически. Не нужно запускать/закрывать браузер руками.

### Sync vs Async

| Sync (используем) | Async | Когда |
|-------------------|-------|-------|
| `page.click(".btn")` | `await page.click(".btn")` | Sync — для тестов, проще |
| `from playwright.sync_api import ...` | `from playwright.async_api import ...` | Async — для скриптов, серверов |

В тестах **всегда sync**. Async усложняет без пользы.

### Сравнение с Selenium

| Selenium | Playwright | Комментарий |
|----------|-----------|-------------|
| `driver = Chrome()` | Авто-фикстура `page` | Не нужен setup/teardown |
| `driver.find_element(By.CSS, ".btn")` | `page.locator(".btn")` | Короче |
| `WebDriverWait(driver, 10).until(...)` | Auto-wait встроен | Не нужны явные ожидания |
| `driver.quit()` | Автоматически | pytest-playwright убирает за собой |
| Только HTTP | HTTP + WebSocket + CDP | Playwright мощнее |
| Нужен chromedriver | Браузеры встроены | `playwright install` и всё |

---

## 2. DOM — Document Object Model

### Что это
DOM — дерево, которое браузер строит из HTML. Каждый тег — узел дерева. Playwright ищет элементы в этом дереве.

```
document
└── html
    ├── head
    │   └── title → "Школа"
    └── body
        ├── header
        │   └── nav
        │       ├── a.logo → "Точка"
        │       └── a.nav-link → "Курсы"
        └── main
            ├── h1 → "Добро пожаловать"
            └── form
                ├── input[name="email"]
                └── button → "Отправить"
```

### Аналогия из Flutter
DOM — как **Widget Tree**. В Flutter: `Scaffold > AppBar > Text`. В браузере: `body > header > nav > a`. Playwright ищет в DOM как `find.byType()` ищет в Widget Tree.

### Инструменты

```bash
# Открыть DevTools → вкладка Elements → видишь DOM
# Правый клик на элемент → "Inspect"
# Console: document.querySelector(".nav-link") → находит элемент
```

---

## 3. Локаторы

### Flutter (ты это знаешь):
```dart
find.byKey(Key('submit-btn'));       // по ключу
find.byType(ElevatedButton);         // по типу виджета
find.text('Отправить');              // по тексту
find.byTooltip('Отправить форму');   // по подсказке
```

### Playwright:
```python
page.get_by_test_id("submit-btn")              # по data-testid — лучший
page.get_by_role("button", name="Отправить")   # по роли + тексту
page.get_by_text("Отправить")                  # по тексту
page.get_by_label("Email")                     # по label input'а
page.get_by_placeholder("Введите email")       # по placeholder
page.locator(".submit-btn")                    # CSS-селектор
page.locator("button:has-text('Отправить')")   # CSS + текст
page.locator("//button[@class='primary']")     # XPath (крайний случай)
```

### Приоритет выбора локатора

```
  Лучший ──────────────────────────────── Худший

  data-testid  >  role  >  label/text  >  CSS  >  XPath
  (стабильный)    (семантика)  (читаемый)   (хрупкий)  (нечитаемый)
```

### Сравнение
| Flutter finder | Playwright locator | Комментарий |
|---------------|-------------------|-------------|
| `find.byKey(Key('id'))` | `page.get_by_test_id("id")` | Самый надёжный |
| `find.byType(Button)` | `page.get_by_role("button")` | По семантической роли |
| `find.text("Текст")` | `page.get_by_text("Текст")` | По видимому тексту |
| `find.byTooltip("tip")` | `page.get_by_title("tip")` | По атрибуту title |
| Нет прямого | `page.get_by_label("Email")` | По связанному label |
| Нет прямого | `page.locator(".class")` | CSS-селектор |

### CSS-селекторы — минимум для тестов

| Селектор | Что находит | Пример |
|---------|-----------|--------|
| `.class` | По классу | `.nav-link` |
| `#id` | По id | `#main-header` |
| `tag` | По тегу | `button`, `input`, `a` |
| `[attr="value"]` | По атрибуту | `[data-testid="submit"]` |
| `parent > child` | Прямой потомок | `nav > a` |
| `ancestor descendant` | Любой потомок | `form input` |
| `:nth-child(2)` | Второй элемент | `li:nth-child(2)` |
| `:has-text("Текст")` | Содержит текст (Playwright) | `button:has-text("Войти")` |

### Подводные камни
1. **CSS-классы меняются** — `.btn-primary-v2-updated` → хрупкий тест. Используй `data-testid`
2. **Текст меняется** — `"Отправить"` → `"Отправить заявку"` → тест падает. `get_by_role` стабильнее
3. **Несколько совпадений** — `page.locator("button")` находит 5 кнопок → нужно уточнить: `.first`, `.nth(2)`, `filter(has_text="...")`

---

## 4. Действия — click, fill, goto

### Flutter (ты это знаешь):
```dart
await tester.tap(find.byKey(Key('submit')));
await tester.enterText(find.byType(TextField), 'hello');
await tester.pumpAndSettle();  // ждём анимации
```

### Playwright:
```python
page.goto("https://example.com")                     # перейти на страницу
page.get_by_label("Email").fill("user@test.com")      # заполнить input
page.get_by_role("button", name="Войти").click()      # кликнуть
page.get_by_label("Пароль").type("secret")             # печатать посимвольно
page.get_by_role("checkbox").check()                   # чекбокс
page.get_by_role("combobox").select_option("option1")  # дропдаун
page.go_back()                                         # назад
page.reload()                                          # перезагрузить
```

### Все основные действия

| Действие | Метод | Комментарий |
|---------|-------|-------------|
| Перейти | `page.goto(url)` | Ждёт загрузку страницы |
| Кликнуть | `.click()` | Ждёт видимость и кликабельность |
| Заполнить | `.fill("text")` | Очищает поле и вводит |
| Печатать | `.type("text")` | Посимвольно, как человек |
| Чекбокс | `.check()` / `.uncheck()` | Идемпотентно |
| Выбор | `.select_option("value")` | `<select>` дропдаун |
| Навести | `.hover()` | Tooltip, подменю |
| Фокус | `.focus()` | Для валидации при потере фокуса |
| Нажать клавишу | `.press("Enter")` | Любая клавиша |
| Загрузить файл | `.set_input_files("path")` | `<input type="file">` |

### Подводные камни
1. **`fill` vs `type`** — `fill` мгновенный (заменяет всё), `type` посимвольный (нужен для автокомплита). В 90% случаев — `fill`
2. **`click` ждёт автоматически** — не нужен `sleep` или `wait`. Playwright сам ждёт пока кнопка станет видимой и кликабельной

---

## 5. Auto-wait — почему не нужны sleep

### Selenium (старый подход):
```python
# Selenium — ручные ожидания, боль
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn"))
)
element.click()
```

### Playwright (наш подход):
```python
# Playwright — всё автоматически
page.locator(".btn").click()   # сам ждёт пока элемент станет кликабельным
```

### Что делает auto-wait перед действием

```
  click() вызван
      │
      ▼
  ┌─ Элемент есть в DOM? ──── нет → ждём (до timeout)
  │     да ▼
  ├─ Видимый? ──────────────── нет → ждём
  │     да ▼
  ├─ Стабильный (не анимируется)? ── нет → ждём
  │     да ▼
  ├─ Принимает события? ──── нет → ждём
  │     да ▼
  └─ КЛИК!
```

### Сравнение
| Selenium | Playwright | Комментарий |
|----------|-----------|-------------|
| `time.sleep(3)` | Не нужен | Auto-wait |
| `WebDriverWait` + `EC.visibility_of` | Встроено | Автоматически |
| Implicit wait (глобально) | `timeout` в конфиге | Один раз настроил |
| Explicit wait (каждый раз) | Не нужен | Playwright сам разбирается |

### Когда всё-таки нужно ждать

```python
# Ждать навигации после клика
page.get_by_role("link", name="Курсы").click()
page.wait_for_url("**/courses")

# Ждать загрузки данных (API-ответ)
with page.expect_response("**/api/courses") as response_info:
    page.get_by_role("button", name="Загрузить").click()
response = response_info.value

# Ждать исчезновения спиннера
page.locator(".spinner").wait_for(state="hidden")
```

### Подводные камни
1. **`time.sleep()` в тестах — антипаттерн** — медленно, ненадёжно. Playwright ждёт умнее
2. **Timeout по умолчанию = 30 сек** — в нашем `config.py`: `timeout: int = 30000`. Если элемент не появился за 30 сек — тест упадёт с понятной ошибкой

---

## 6. Assertions — expect API

### Flutter (ты это знаешь):
```dart
expect(find.text('Hello'), findsOneWidget);
expect(find.byType(Button), findsNothing);
```

### Playwright:
```python
from playwright.sync_api import expect

# Страница
expect(page).to_have_title("Школа")
expect(page).to_have_url(re.compile(r"/courses"))

# Элемент — видимость
expect(page.locator(".header")).to_be_visible()
expect(page.locator(".spinner")).to_be_hidden()

# Текст
expect(page.locator("h1")).to_have_text("Добро пожаловать")
expect(page.locator(".error")).to_contain_text("Ошибка")

# Атрибуты
expect(page.locator("input")).to_have_value("user@test.com")
expect(page.locator(".btn")).to_be_enabled()
expect(page.locator(".btn")).to_be_disabled()

# Количество
expect(page.locator(".card")).to_have_count(5)

# Отрицание — добавляй not_to
expect(page.locator(".error")).not_to_be_visible()
```

### Сравнение
| Flutter | Playwright | Что проверяет |
|---------|-----------|--------------|
| `findsOneWidget` | `to_be_visible()` | Элемент есть |
| `findsNothing` | `not_to_be_visible()` | Элемента нет |
| `expect(widget.text, equals("Hi"))` | `to_have_text("Hi")` | Текст совпадает |
| Нет прямого | `to_have_url(...)` | URL страницы |

### `expect` vs `assert`

| `expect` (Playwright) | `assert` (Python) |
|----------------------|-------------------|
| **Ждёт** — повторяет проверку до timeout | **Мгновенный** — проверяет один раз |
| `expect(loc).to_be_visible()` | `assert loc.is_visible()` |
| Для UI — элементы появляются не сразу | Для API — ответ уже есть |

Для UI **всегда `expect`**, не `assert` — элемент может ещё загружаться.

### Подводные камни
1. **`assert` вместо `expect`** для UI → тест мгновенно проверяет и падает, не дождавшись элемента
2. **`to_have_text` vs `to_contain_text`** — первый проверяет полное совпадение, второй — подстроку
3. **Regex** — `expect(page).to_have_url(re.compile(r"/courses"))` — не забудь `import re`

---

## 7. POM — Page Object Model

### Ассоциация
POM — как **пульт от телевизора**. Не ты жмёшь кнопки на телевизоре напрямую, а через пульт. Тест → Page Object → браузер. Изменился интерфейс телевизора → обновил пульт, тесты не трогаешь.

### Flutter (ты это знаешь):
```dart
// В Flutter обычно тестируешь виджеты напрямую, но для интеграционных:
class LoginPage {
  final WidgetTester tester;
  LoginPage(this.tester);

  Future<void> enterEmail(String email) async {
    await tester.enterText(find.byKey(Key('email')), email);
  }
  Future<void> tapLogin() async {
    await tester.tap(find.byKey(Key('login-btn')));
    await tester.pumpAndSettle();
  }
}
```

### Playwright:
```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Пароль")
        self.login_button = page.get_by_role("button", name="Войти")

    def goto(self):
        self.page.goto("/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
```

### Тест с POM

```python
def test_successful_login(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("user@test.com", "password123")
    expect(page).to_have_url(re.compile(r"/dashboard"))
```

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Локаторы в `__init__` | Локаторы в каждом методе | Дублирование, сложнее менять |
| Один Page Object = одна страница | Один на весь сайт | Гигантский файл, невозможно поддерживать |
| Методы — действия (`login`, `search`) | Методы — клики (`click_button_3`) | Нечитаемый тест |
| Page Object **не делает assert** | `assert` внутри Page Object | Смешиваешь действия и проверки |

---

## 8. Паттерны тестирования

### Наш 3-слойный паттерн

```
  ┌──────────────────┐
  │    TEST FILE     │  ← только флоу: page.action() + check.verify()
  │  test_login.py   │     никаких селекторов, assert, if/else
  └────────┬─────────┘
           │
  ┌────────▼─────────┐
  │   PAGE OBJECT    │  ← действия: fill, click, goto
  │  login_page.py   │     знает селекторы, не знает проверки
  └────────┬─────────┘
           │
  ┌────────▼─────────┐
  │     CHECKS       │  ← проверки: assert, expect
  │  login_checks.py │     знает что проверять, не знает как действовать
  └──────────────────┘
```

### Почему 3 слоя, а не 2 (POM)

| 2 слоя (классический POM) | 3 слоя (наш паттерн) | Плюс |
|--------------------------|---------------------|------|
| Page Object содержит assert | Checks отдельно | Page Object переиспользуется без привязки к проверкам |
| Тест вызывает page + assert | Тест вызывает page + check | Чёткое разделение ответственности |
| Упал тест → ищи в Page Object | Упал тест → смотри Checks | Быстрее находишь проблему |

### Паттерны из Notion

**Page Object** — описан выше. Инкапсулирует страницу.

**Factory Method** — создание Page Object через фабрику:
```python
# conftest.py
@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)        # фабрика — фикстура создаёт объект

# тест
def test_login(login_page):       # получаешь готовый объект
    login_page.goto()
    login_page.login("user", "pass")
```

**Data-Driven** — данные управляют тестом:
```python
@pytest.mark.parametrize("email, password, expected", [
    ("valid@test.com", "pass123", "/dashboard"),
    ("", "pass123", "/login"),                      # пустой email
    ("valid@test.com", "", "/login"),                # пустой пароль
])
def test_login(login_page, email, password, expected):
    login_page.goto()
    login_page.login(email, password)
    expect(login_page.page).to_have_url(re.compile(expected))
```

---

## 9. pytest-playwright — авто-фикстуры

### Встроенные фикстуры

| Фикстура | scope | Что даёт |
|----------|-------|---------|
| `browser` | session | Экземпляр браузера (один на все тесты) |
| `context` | function | Изолированный контекст (куки, storage) |
| `page` | function | Вкладка в браузере (новая для каждого теста) |
| `browser_name` | session | `"chromium"`, `"firefox"`, `"webkit"` |

### Запуск

```bash
pytest                               # Chromium (по умолчанию)
pytest --browser firefox             # Firefox
pytest --browser webkit              # Safari
pytest --browser chromium --browser firefox  # оба
pytest --headed                      # с GUI (видишь браузер)
pytest --slowmo 500                  # задержка 500мс между действиями
```

### Настройка через conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True,             # из config.py
    }
```

---

## 10. Browser contexts — изоляция

### Что это
Context — как **вкладка инкогнито**. Свои куки, localStorage, сессия. Каждый тест получает чистый context = полная изоляция.

### Аналогия из Flutter
В Flutter `testWidgets` создаёт чистый Widget Tree для каждого теста. В Playwright `context` — чистый браузерный "мир" для каждого теста.

### Зачем

```
Тест 1: логинится как admin     → context 1 (свои куки)
Тест 2: логинится как user      → context 2 (свои куки)
Тест 3: без логина              → context 3 (пустые куки)
```

Тесты не мешают друг другу. Нет `logout()` между тестами — просто новый контекст.

### Несколько вкладок/пользователей

```python
def test_chat_between_users(browser):
    # два контекста = два пользователя
    context_admin = browser.new_context()
    context_user = browser.new_context()

    page_admin = context_admin.new_page()
    page_user = context_user.new_page()

    page_admin.goto("/chat")
    page_user.goto("/chat")
    # каждый видит свою сессию
```

---

## 11. Скриншоты и видео

### Скриншот при падении

```python
# conftest.py
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
```

### Видео

```python
# conftest.py — включаем запись
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
    }
```

```bash
# или через CLI
pytest --video on                    # всегда
pytest --video retain-on-failure     # только при падении
```

### Скриншот вручную

```python
page.screenshot(path="debug.png")                            # вся страница
page.screenshot(path="debug.png", full_page=True)            # с прокруткой
page.locator(".card").screenshot(path="card.png")             # один элемент
```

---

## 12. Allure — интеграция для UI

### Те же декораторы что и для API

```python
@allure.feature("Навигация")
class TestNavigation:

    @allure.story("Главная страница")
    @allure.title("Проверка заголовка")
    def test_main_title(self, page: Page):
        page.goto("/")
        expect(page.locator("h1")).to_have_text("Школа")
```

### Шаги в Check-классах

```python
class NavigationChecks:
    @allure.step("Проверка: заголовок = '{expected}'")
    def check_title(self, page: Page, expected: str):
        expect(page.locator("h1")).to_have_text(expected)

    @allure.step("Проверка: URL содержит '{path}'")
    def check_url(self, page: Page, path: str):
        expect(page).to_have_url(re.compile(path))
```

### Скриншот в шаге

```python
@allure.step("Проверка: секция видна")
def check_section_visible(self, page: Page, selector: str):
    locator = page.locator(selector)
    expect(locator).to_be_visible()
    allure.attach(
        page.screenshot(),
        name="current_state",
        attachment_type=allure.attachment_type.PNG
    )
```

---

## 13. 3-слойная архитектура — реализация для UI

### Структура проекта

```
tests/ui/
├── conftest.py              ← фикстуры: page, navigation_page, checks
├── test_data.py             ← URL, тексты, селекторы тестов
│
├── locators/
│   ├── main_locators.py     ← только селекторы, без логики
│   └── nav_locators.py
│
├── pages/
│   ├── base_page.py         ← общие методы (goto, wait)
│   ├── main_page.py         ← действия на главной
│   └── nav_page.py          ← навигация
│
├── checks/
│   ├── main_checks.py       ← проверки главной
│   └── nav_checks.py        ← проверки навигации
│
├── test_navigation.py       ← тесты навигации
├── test_main.py             ← тесты главной
└── test_form.py             ← тесты формы
```

### Слой 1: Locators — только селекторы

```python
# locators/nav_locators.py
class NavLocators:
    LOGO = "[data-testid='logo']"
    COURSES_LINK = "a[href='/courses']"
    MENU_BUTTON = "[data-testid='menu-btn']"
```

Никакой логики. Изменился селектор → правишь одну строку, не 20 тестов.

### Слой 2: Pages — только действия

```python
# pages/base_page.py
class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        self.page.goto(path)

# pages/nav_page.py
from tests.ui.locators.nav_locators import NavLocators

class NavPage(BasePage):
    def click_logo(self):
        self.page.locator(NavLocators.LOGO).click()

    def go_to_courses(self):
        self.page.locator(NavLocators.COURSES_LINK).click()

    def open_menu(self):
        self.page.locator(NavLocators.MENU_BUTTON).click()
```

Никаких assert. Страница **делает**, не **проверяет**.

### Слой 3: Checks — только проверки

```python
# checks/nav_checks.py
class NavChecks:
    @allure.step("Проверка: открылась страница курсов")
    def check_courses_opened(self, page: Page):
        expect(page).to_have_url(re.compile(r"/courses"))
        expect(page.locator("h1")).to_contain_text("Курсы")

    @allure.step("Проверка: логотип ведёт на главную")
    def check_logo_leads_home(self, page: Page):
        expect(page).to_have_url(re.compile(r"/$"))
```

Никаких click/fill. Checks **проверяет**, не **действует**.

### Тест — только флоу

```python
# test_navigation.py
@allure.feature("Навигация")
class TestNavigation:

    @allure.title("Клик по логотипу ведёт на главную")
    def test_logo_leads_home(self, nav_page, nav_checks, page):
        nav_page.goto("/courses")       # действие
        nav_page.click_logo()           # действие
        nav_checks.check_logo_leads_home(page)  # проверка
```

Тест читается как **сценарий**: зашёл → кликнул → проверил.

### Фикстуры

```python
# tests/ui/conftest.py
@pytest.fixture
def nav_page(page: Page):
    return NavPage(page)

@pytest.fixture
def nav_checks(page: Page):
    return NavChecks(page)     # checks нужен page для expect/locator
```

---
---

# НАВИГАЦИЯ

| Файл | Что внутри |
|------|-----------|
| [00 — Шпаргалка для собеса](00_interview_cheatsheet.md) | Определения + подвох-вопросы |
| [01 — Python язык](01_python_language.md) | Подробный разбор с Dart-мостиком |
| [02 — API-тестирование](02_api_testing.md) | requests + pytest + Pydantic |
| **03 — UI-тестирование** | **Ты здесь** |
