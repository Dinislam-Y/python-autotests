# Python QA Autotest Project — Задачи

> Проект: `python-autotests`
> Стек: pytest + Playwright + requests + Allure + Docker + GitHub Actions
> UI: cms-dev.tochka-school.ru (лендинг Точка Знаний) | API: reqres.in
> Путь: `/Users/dinislam/StudioProjects/python-autotests/`
>
> **Архитектура**: 3-файловое разделение (Locators / Page / Check) — адаптация паттерна из Flutter QA
> **Витрина**: проект-портфолио + proof of concept для текущего работодателя (Python+Playwright для нашего продукта)
> **Стиль кода**: комментарии от первого лица, нетривиальные

---

## Структура проекта (финальная)

```
python-autotests/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   ├── conftest.py                        # Общие фикстуры (settings)
│   ├── api/
│   │   ├── conftest.py                    # API-фикстуры (api_client)
│   │   ├── test_data.py                   # Константы — как Dependencies во Flutter
│   │   ├── models.py                      # Pydantic-модели ответов API
│   │   ├── checks/
│   │   │   ├── user_checks.py             # Ассерты для /users
│   │   │   └── auth_checks.py             # Ассерты для /register, /login
│   │   ├── test_users.py                  # Тест-флоу: CRUD users
│   │   ├── test_register.py               # Тест-флоу: регистрация/логин
│   │   └── test_resources.py              # Тест-флоу: ресурсы + параметризация
│   └── ui/
│       ├── conftest.py                    # UI-фикстуры (page objects, auto-screenshot)
│       ├── test_data.py                   # Константы: URL разделов, ожидаемые тексты
│       ├── locators/
│       │   ├── header_locators.py         # Меню, навигация, логотип
│       │   ├── main_page_locators.py      # Главная: баннер, категории, CTA
│       │   ├── courses_locators.py        # Каталог курсов: фильтры, карточки
│       │   ├── form_locators.py           # Форма записи: поля, чекбоксы, кнопка
│       │   └── footer_locators.py         # Футер: ссылки, соцсети, документы
│       ├── pages/
│       │   ├── base_page.py               # Базовый Page Object
│       │   ├── header_page.py             # Навигация по меню
│       │   ├── main_page.py               # Действия на главной
│       │   ├── courses_page.py            # Каталог: фильтрация, выбор
│       │   ├── form_page.py               # Заполнение формы записи
│       │   └── footer_page.py             # Действия в футере
│       ├── checks/
│       │   ├── header_checks.py           # Проверки навигации
│       │   ├── main_page_checks.py        # Проверки главной
│       │   ├── courses_checks.py          # Проверки каталога
│       │   ├── form_checks.py             # Проверки формы
│       │   └── footer_checks.py           # Проверки футера
│       ├── test_navigation.py             # Тесты навигации по разделам
│       ├── test_main_page.py              # Тесты главной страницы
│       ├── test_courses.py                # Тесты каталога курсов
│       ├── test_enrollment_form.py        # Тесты формы записи
│       └── test_footer.py                 # Тесты футера и ссылок
├── utils/
│   ├── api_client.py                      # HTTP-обёртка с логированием
│   └── helpers.py                         # Faker и утилиты
├── config/
│   ├── config.py                          # Pydantic Settings
│   └── .env.example
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .gitignore
└── README.md
```

### Правила архитектуры (адаптировано из Flutter)

| Правило | Описание |
|---------|----------|
| **Locators** — только селекторы | Класс с константами CSS/data-test селекторов. Никакой логики |
| **Page** — только действия | Методы: click, fill, navigate. Никаких assert. Ожидания — внутри методов |
| **Check** — только проверки | Методы с assert. Каждый метод проверяет уникальное условие |
| **Test** — только флоу | Вызывает page.action() и check.verify(). Никаких селекторов, ассертов, if/else |
| **test_data** — только константы | Как Dependencies во Flutter. Никакого хардкода в тестах |
| **Мутационная устойчивость** | Exact counts, уникальные проверки в каждом check-методе |
| **Человеческий стиль** | Комментарии от первого лица, естественные, как в процессе разработки |

---

## Этап 1: Инициализация проекта

### 1.1 Git и структура папок
- [ ] `git init` в директории `python-autotests`
- [ ] Создать `.gitignore`:
  ```
  __pycache__/
  .venv/
  *.pyc
  .env
  allure-results/
  allure-report/
  .pytest_cache/
  test-results/
  .ruff_cache/
  ```
- [ ] Создать структуру директорий:
  ```
  mkdir -p tests/api/checks tests/ui/locators tests/ui/pages tests/ui/checks config utils .github/workflows
  ```
- [ ] Создать `__init__.py` в: `tests/`, `tests/api/`, `tests/api/checks/`, `tests/ui/`, `tests/ui/locators/`, `tests/ui/pages/`, `tests/ui/checks/`, `config/`, `utils/`

### 1.2 Виртуальное окружение и зависимости
- [ ] Создать venv: `python3 -m venv .venv`
- [ ] Активировать: `source .venv/bin/activate`
- [ ] Создать `pyproject.toml`:
  - `[project]` — name=`python-autotests`, version=`0.1.0`, requires-python=`>=3.9`
  - `[project.dependencies]`:
    - `pytest>=8.0`
    - `playwright`
    - `pytest-playwright`
    - `requests`
    - `pydantic>=2.0`
    - `pydantic-settings`
    - `allure-pytest`
    - `faker`
    - `python-dotenv`
  - `[project.optional-dependencies]` → dev: `ruff`
  - `[tool.pytest.ini_options]`:
    - markers: `api`, `ui`, `smoke`
    - addopts: `-v --tb=short`
  - `[tool.ruff]` — line-length=120
- [ ] `pip install -e ".[dev]"`
- [ ] `playwright install chromium`

### 1.3 Конфигурация проекта
- [ ] Создать `config/config.py`:
  - `Settings(BaseSettings)`:
    - `base_url_ui: str = "https://cms-dev.tochka-school.ru"`
    - `base_url_api: str = "https://reqres.in"`
    - `browser: str = "chromium"`
    - `headless: bool = True`
    - `timeout: int = 30000`
  - `model_config = SettingsConfigDict(env_file=".env")`
  - `settings = Settings()`
- [ ] Создать `config/.env.example`

### 1.4 Базовый conftest.py
- [ ] Создать `tests/conftest.py`:
  - Фикстура `settings` (scope=session)
- [ ] Проверить: `pytest --collect-only`

### 1.5 Первый коммит
- [ ] `git add .` + коммит `"init: project structure, deps, config"`

---

## Этап 2: API тесты (reqres.in)

### 2.1 HTTP-клиент
- [ ] Создать `utils/api_client.py`:
  - Класс `ApiClient(base_url)`:
    - `self.session = requests.Session()`
    - Методы: `get(path)`, `post(path, json)`, `put(path, json)`, `patch(path, json)`, `delete(path)`
    - Логирование каждого запроса: метод + url + status_code

### 2.2 Тестовые данные
- [ ] Создать `tests/api/test_data.py`:
  ```python
  EXISTING_USER_ID = 2
  NON_EXISTING_USER_ID = 23
  VALID_EMAIL = "eve.holt@reqres.in"
  VALID_PASSWORD = "pistol"
  CREATE_USER_NAME = "morpheus"
  CREATE_USER_JOB = "leader"
  UPDATE_USER_JOB = "zion resident"
  ```

### 2.3 Pydantic-модели ответов
- [ ] Создать `tests/api/models.py`:
  - `UserData` — id, email, first_name, last_name, avatar
  - `SingleUserResponse` — data: UserData, support: dict
  - `UserListResponse` — page, per_page, total, data: list[UserData]
  - `CreateUserResponse` — name, job, id, createdAt

### 2.4 API Check-классы
- [ ] Создать `tests/api/checks/user_checks.py`:
  - Класс `UserChecks`:
    - `check_user_found(response, user_id)` — status=200, id совпадает, валидация SingleUserResponse
    - `check_user_list(response, expected_page)` — status=200, data не пуст, page совпадает
    - `check_user_not_found(response)` — status=404
    - `check_user_created(response, name, job)` — status=201, id есть, name/job совпадают
    - `check_user_updated(response)` — status=200
    - `check_user_deleted(response)` — status=204
- [ ] Создать `tests/api/checks/auth_checks.py`:
  - Класс `AuthChecks`:
    - `check_register_success(response)` — status=200, token есть, id есть
    - `check_register_error(response, expected_error)` — status=400, error совпадает
    - `check_login_success(response)` — status=200, token есть
    - `check_login_error(response, expected_error)` — status=400, error совпадает

### 2.5 API-фикстуры
- [ ] Создать `tests/api/conftest.py`:
  - Фикстура `api_client` (scope=session) → `ApiClient(settings.base_url_api)`
  - Фикстура `user_checks` → `UserChecks()`
  - Фикстура `auth_checks` → `AuthChecks()`

### 2.6 Тесты CRUD пользователей
- [ ] Создать `tests/api/test_users.py`:
  - Тест-файл — **только флоу**, никаких `assert`:
    ```python
    def test_get_single_user(api_client, user_checks):
        response = api_client.get(f"/api/users/{EXISTING_USER_ID}")
        user_checks.check_user_found(response, EXISTING_USER_ID)
    ```
  - Тесты: `test_get_single_user`, `test_get_users_list`, `test_user_not_found`, `test_create_user`, `test_update_user_put`, `test_update_user_patch`, `test_delete_user`

### 2.7 Тесты регистрации/логина
- [ ] Создать `tests/api/test_register.py`:
  - `test_register_successful`, `test_register_missing_password`, `test_login_successful`, `test_login_missing_password`

### 2.8 Тесты ресурсов с параметризацией
- [ ] Создать `tests/api/test_resources.py`:
  - `@pytest.mark.parametrize("resource_id", [1, 2, 3])`
  - `test_get_resource_by_id`, `test_resource_not_found`, `test_resources_list_pagination`

### 2.9 Запуск и проверка
- [ ] `pytest tests/api/ -v` — все зелёные
- [ ] `pytest tests/api/ -v -m api` — маркер работает
- [ ] Коммит: `"feat: API tests — CRUD, auth, parametrize, check-classes"`

---

## Этап 3: UI — Locators / Pages / Checks (Точка Знаний)

### 3.1 Тестовые данные UI
- [ ] Создать `tests/ui/test_data.py`:
  ```python
  # cms-dev.tochka-school.ru — разделы и ожидаемые значения
  BASE_URL = "https://cms-dev.tochka-school.ru"

  # навигация — внутренние страницы
  COURSES_URL = "/filter_courses"
  SUMMER_COURSES_URL = "/summer_course"
  BLOG_URL = "/blog"
  OGE_URL = "/oge"
  EGE_URL = "/ege"
  FAMILY_EDUCATION_URL = "/so"
  IT_COURSES_URL = "/it"

  # возрастные категории
  AGE_CATEGORIES = {
      "doshkolniki": "/doshkolniki",
      "nachalnaya-shkola": "/nachalnaya-shkola",
      "srednyaya-shkola": "/srednyaya-shkola",
      "starshaya-shkola": "/starshaya-shkola",
  }

  # предметы (примеры для параметризации)
  COURSE_SUBJECTS = [
      "matematika",
      "angliyskiy-yazyk",
      "russkiy-yazyk",
  ]

  # форма записи
  VALID_PHONE = "+7 (999) 123-45-67"
  INVALID_PHONE = "123"

  # ожидаемые тексты
  MAIN_PAGE_TITLE_CONTAINS = "Точка"
  FOOTER_LICENSE_TEXT_CONTAINS = "Лицензия"
  ```

### 3.2 Locators — Header / Navigation
- [ ] Создать `tests/ui/locators/header_locators.py`:
  - `LOGO` — логотип (ссылка на главную)
  - `NAV_ALL_COURSES` — "Все курсы" в меню
  - `NAV_SUMMER_COURSES` — "Летние курсы"
  - `NAV_BLOG` — "Блог"
  - `NAV_ENROLLMENT_BUTTON` — "Подобрать занятия" (открывает модалку/форму)
  - `NAV_LOGIN_BUTTON` — "Вход в личный кабинет"
  - Возрастные категории: `NAV_PRESCHOOL`, `NAV_PRIMARY`, `NAV_MIDDLE`, `NAV_HIGH`

### 3.3 Locators — Main Page
- [ ] Создать `tests/ui/locators/main_page_locators.py`:
  - `HERO_BANNER` — главный баннер
  - `AGE_CATEGORY_CARDS` — карточки "дошкольники / начальная / средняя / старшая"
  - `DIRECTION_BLOCKS` — блоки направлений (школьные предметы, IT, языки)
  - `REVIEWS_SECTION` — секция отзывов
  - `REVIEW_ITEMS` — отдельные отзывы (для подсчёта)
  - `CTA_BUTTONS` — кнопки "Записаться" / "Перейти" на главной

### 3.4 Locators — Courses Catalog
- [ ] Создать `tests/ui/locators/courses_locators.py`:
  - `COURSE_CARD` — карточка курса
  - `COURSE_TITLE` — название курса в карточке
  - `FILTER_AGE` — фильтр по возрасту (если есть)
  - `FILTER_SUBJECT` — фильтр по предмету (если есть)

### 3.5 Locators — Enrollment Form
- [ ] Создать `tests/ui/locators/form_locators.py`:
  - `FORM_CONTAINER = ".pre_n_form"` — контейнер формы
  - `CLASS_SELECT` — селект класса (дошкольник, 1-11)
  - `PHONE_INPUT = "[data-phone-pattern]"` — поле телефона с маской
  - `CONSENT_CHECKBOX` — чекбокс согласия на обработку данных
  - `NEWSLETTER_CHECKBOX` — чекбокс рассылки
  - `SUBMIT_BUTTON = ".btn-warning"` — кнопка "Записаться"
  - `VALIDATION_ERROR` — сообщение об ошибке валидации (если есть)

### 3.6 Locators — Footer
- [ ] Создать `tests/ui/locators/footer_locators.py`:
  - `FOOTER` — контейнер футера
  - `SOCIAL_LINKS` — ссылки соцсетей (Telegram, VK, YouTube)
  - `DOCUMENTS_LINKS` — ссылки на документы (политика, оферта)
  - `LICENSE_TEXT` — текст лицензии
  - `BLOG_LINK` — ссылка на блог из футера
  - `CONTACTS_LINK` — контакты

### 3.7 Base Page
- [ ] Создать `tests/ui/pages/base_page.py`:
  - `BasePage(page: Page)`:
    - `open(url)` — goto с ожиданием
    - `get_title() -> str`
    - `get_current_url() -> str`
    - `scroll_to_element(selector)` — для lazy-load элементов

### 3.8 Pages — Header, Main, Courses, Form, Footer
- [ ] Создать `tests/ui/pages/header_page.py`:
  - `HeaderPage(BasePage)` — использует `HeaderLocators`
  - Методы:
    - `click_logo()`
    - `go_to_all_courses()`
    - `go_to_summer_courses()`
    - `go_to_blog()`
    - `open_enrollment_form()` — клик по "Подобрать занятия"
    - `go_to_age_category(category_name)`
  - Ожидания внутри каждого метода
  - `@allure.step` на каждом

- [ ] Создать `tests/ui/pages/main_page.py`:
  - `MainPage(BasePage)` — использует `MainPageLocators`
  - Методы:
    - `open()` — goto BASE_URL
    - `get_age_category_cards_count() -> int`
    - `click_age_category(index)`
    - `get_direction_blocks_count() -> int`
    - `scroll_to_reviews()`
    - `get_reviews_count() -> int`

- [ ] Создать `tests/ui/pages/courses_page.py`:
  - `CoursesPage(BasePage)` — использует `CoursesLocators`
  - Методы:
    - `open()` — goto /filter_courses
    - `get_course_cards_count() -> int`
    - `get_course_titles() -> list[str]`
    - `open_course_by_subject(subject_slug)` — goto /filter_courses/{subject}

- [ ] Создать `tests/ui/pages/form_page.py`:
  - `FormPage(BasePage)` — использует `FormLocators`
  - Методы:
    - `select_class(value)` — выбор класса
    - `fill_phone(phone)` — ввод телефона (маска!)
    - `check_consent()` — клик чекбокса
    - `check_newsletter()` — клик рассылки
    - `submit()` — клик "Записаться"
    - `is_form_visible() -> bool`

- [ ] Создать `tests/ui/pages/footer_page.py`:
  - `FooterPage(BasePage)` — использует `FooterLocators`
  - Методы:
    - `scroll_to_footer()`
    - `get_social_links_count() -> int`
    - `get_document_links_count() -> int`
    - `click_document_link(index)`

### 3.9 Checks — Header
- [ ] Создать `tests/ui/checks/header_checks.py`:
  - `HeaderChecks(page)`:
    - `check_navigated_to(expected_url_part)` — URL содержит path
    - `check_page_loaded()` — title не пустой, нет ошибок загрузки
    - `check_returned_to_main()` — URL = BASE_URL

### 3.10 Checks — Main Page
- [ ] Создать `tests/ui/checks/main_page_checks.py`:
  - `MainPageChecks(page)`:
    - `check_hero_banner_visible()` — баннер отображается
    - `check_age_categories_displayed(expected_count)` — точное кол-во (4 категории)
    - `check_direction_blocks_present(min_count)` — есть направления
    - `check_reviews_loaded(min_count)` — отзывы загрузились
    - `check_title_contains(text)` — заголовок страницы

### 3.11 Checks — Courses
- [ ] Создать `tests/ui/checks/courses_checks.py`:
  - `CoursesChecks(page)`:
    - `check_courses_displayed(min_count)` — курсы есть на странице
    - `check_course_titles_not_empty(titles)` — у каждого курса есть название
    - `check_on_courses_page()` — URL содержит /filter_courses

### 3.12 Checks — Form
- [ ] Создать `tests/ui/checks/form_checks.py`:
  - `FormChecks(page)`:
    - `check_form_visible()` — форма отображается
    - `check_phone_mask_applied()` — маска телефона работает
    - `check_consent_required()` — без согласия нельзя отправить (если валидация есть)

### 3.13 Checks — Footer
- [ ] Создать `tests/ui/checks/footer_checks.py`:
  - `FooterChecks(page)`:
    - `check_footer_visible()` — футер виден после скролла
    - `check_social_links_count(expected)` — точное кол-во соцсетей
    - `check_documents_present(min_count)` — документы есть
    - `check_license_text_contains(text)` — текст лицензии

### 3.14 UI-фикстуры
- [ ] Создать `tests/ui/conftest.py`:
  - Page фикстуры: `header_page`, `main_page`, `courses_page`, `form_page`, `footer_page`
  - Check фикстуры: `header_checks`, `main_page_checks`, `courses_checks`, `form_checks`, `footer_checks`
  - Хук: скриншот при падении → allure attach

### 3.15 Коммит
- [ ] Коммит: `"feat: UI architecture — locators, pages, checks for tochka-school.ru"`

---

## Этап 4: UI тесты (Точка Знаний)

> **Правило: тест-файлы содержат ТОЛЬКО флоу.**
> Никаких селекторов, assert, if/else, явных ожиданий.
> Только вызовы `page.action()` и `check.verify()`.

### 4.1 Тесты навигации
- [ ] Создать `tests/ui/test_navigation.py`:
  ```python
  @pytest.mark.smoke
  def test_main_page_opens(main_page, main_page_checks):
      main_page.open()
      main_page_checks.check_title_contains(MAIN_PAGE_TITLE_CONTAINS)
      main_page_checks.check_hero_banner_visible()

  @pytest.mark.parametrize("url_path", [
      COURSES_URL, SUMMER_COURSES_URL, BLOG_URL, OGE_URL, EGE_URL,
  ])
  def test_section_pages_accessible(main_page, header_page, header_checks, url_path):
      main_page.open()
      header_page.go_to_section(url_path)
      header_checks.check_navigated_to(url_path)
      header_checks.check_page_loaded()

  @pytest.mark.parametrize("category,path", AGE_CATEGORIES.items())
  def test_age_category_navigation(main_page, header_page, header_checks, category, path):
      main_page.open()
      header_page.go_to_age_category(category)
      header_checks.check_navigated_to(path)

  def test_logo_returns_to_main(main_page, header_page, header_checks):
      main_page.open()
      header_page.go_to_all_courses()
      header_page.click_logo()
      header_checks.check_returned_to_main()
  ```

### 4.2 Тесты главной страницы
- [ ] Создать `tests/ui/test_main_page.py`:
  - `test_hero_banner_displayed` — баннер видим
  - `test_age_categories_shown` — ровно 4 категории по возрасту
  - `test_direction_blocks_present` — направления обучения отображаются
  - `test_reviews_section_loaded` — отзывы загрузились (min 3)
  - `test_cta_buttons_visible` — кнопки призыва к действию на месте

### 4.3 Тесты каталога курсов
- [ ] Создать `tests/ui/test_courses.py`:
  - `test_courses_page_loads` — /filter_courses открывается, курсы есть
  - `test_course_cards_have_titles` — у каждой карточки есть название
  - `@pytest.mark.parametrize("subject", COURSE_SUBJECTS)`:
    - `test_subject_page_accessible` — /filter_courses/{subject} открывается

### 4.4 Тесты формы записи
- [ ] Создать `tests/ui/test_enrollment_form.py`:
  - `test_enrollment_form_visible` — форма "Подобрать занятия" отображается
  - `test_phone_mask_works` — маска телефона применяется при вводе
  - `test_class_selection` — можно выбрать класс из списка
  - **НЕ** отправляем форму реально (dev-окружение) — проверяем только UI-поведение

### 4.5 Тесты футера
- [ ] Создать `tests/ui/test_footer.py`:
  - `test_footer_visible` — футер отображается
  - `test_social_links_present` — соцсети (Telegram, VK, YouTube) есть
  - `test_documents_links_present` — ссылки на документы (политика, оферта)
  - `test_license_info_displayed` — информация о лицензии видна

### 4.6 Запуск и проверка
- [ ] `pytest tests/ui/ -v --headed` — визуально проверить
- [ ] `pytest tests/ui/ -v` — headless, все зелёные
- [ ] `pytest tests/ui/ -v -m smoke` — smoke-набор работает
- [ ] Коммит: `"feat: UI tests — navigation, main page, courses, form, footer"`

---

## Этап 5: Allure отчётность

### 5.1 Базовая интеграция
- [ ] Добавить `addopts = "--alluredir=allure-results"` в pyproject.toml
- [ ] `pytest tests/ -v` → `allure-results/` создалась
- [ ] `brew install allure` (если не установлен)
- [ ] `allure serve allure-results` — отчёт открывается

### 5.2 Декораторы в API тестах
- [ ] `@allure.feature("Users API")` / `@allure.feature("Auth API")`
- [ ] `@allure.story("Create user")` на каждом тесте
- [ ] `@allure.title("Создание пользователя")` — человекочитаемые названия
- [ ] `@allure.severity(CRITICAL)` для ключевых

### 5.3 Декораторы в UI тестах
- [ ] `@allure.feature("Навигация")` / `@allure.feature("Главная страница")` / `@allure.feature("Каталог курсов")` / `@allure.feature("Форма записи")` / `@allure.feature("Футер")`
- [ ] `@allure.story(...)` и `@allure.title(...)` для каждого теста
- [ ] `@allure.severity(CRITICAL)` для навигации и формы, `NORMAL` для контентных

### 5.4 Allure steps в Page и Check методах
- [ ] `@allure.step` на всех публичных методах Pages и Checks
- [ ] Примеры:
  - `@allure.step("Переход в раздел: {section}")` на `HeaderPage.go_to_section()`
  - `@allure.step("Открытие главной страницы")` на `MainPage.open()`
  - `@allure.step("Заполнение телефона: {phone}")` на `FormPage.fill_phone()`
  - `@allure.step("Проверка: баннер отображается")` на `MainPageChecks.check_hero_banner_visible()`

### 5.5 Скриншоты при падении
- [ ] В `tests/ui/conftest.py` — хук `pytest_runtest_makereport`:
  - При failed: `allure.attach(page.screenshot(), "screenshot", PNG)`

### 5.6 Вложения API
- [ ] В `ApiClient` — `allure.attach(response body, "Response", JSON)` на каждый запрос

### 5.7 Проверка и коммит
- [ ] `allure serve allure-results` — features, stories, steps, скриншоты видны
- [ ] Коммит: `"feat: Allure — steps, screenshots on failure, API attachments"`

---

## Этап 6: Docker

### 6.1 Dockerfile
- [ ] Базовый образ: `mcr.microsoft.com/playwright/python:v1.49.0-noble`
- [ ] `COPY pyproject.toml . && pip install -e "."`
- [ ] `COPY . .`
- [ ] `CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]`

### 6.2 docker-compose.yml
- [ ] Service `tests`: build + volume `./allure-results:/app/allure-results`

### 6.3 .dockerignore
- [ ] `.venv/`, `__pycache__/`, `.git/`, `allure-results/`, `allure-report/`

### 6.4 Проверка
- [ ] `docker-compose build` — собирается
- [ ] `docker-compose up` — тесты проходят
- [ ] `allure serve allure-results` — отчёт на хосте
- [ ] Коммит: `"feat: Docker — containerized test execution"`

---

## Этап 7: GitHub Actions CI

### 7.1 GitHub репозиторий
- [ ] `gh repo create python-autotests --public --source=. --push`

### 7.2 Workflow
- [ ] `.github/workflows/tests.yml`:
  - Python 3.12, install deps, install playwright chromium, run tests
  - Upload allure-results artifact
  - Allure Report action → deploy to GitHub Pages

### 7.3 GitHub Pages
- [ ] Settings → Pages → source: gh-pages branch

### 7.4 Проверка
- [ ] `git push` → Actions зелёные
- [ ] Allure Report на GitHub Pages доступен
- [ ] Коммит (если правки): `"feat: CI — GitHub Actions + Allure Pages"`

---

## Этап 8: Финализация

### 8.1 README.md
- [ ] Заголовок + бейджи (CI status, Python)
- [ ] Описание: автотесты для лендинга Точка Знаний + API-тесты reqres.in
- [ ] Стек и архитектура (3-layer pattern из Flutter-опыта)
- [ ] Структура проекта (дерево)
- [ ] Quick start: clone → install → run
- [ ] Docker: `docker-compose up`
- [ ] Allure: ссылка на GitHub Pages
- [ ] **Стиль README**: от первого лица, профессионально но живо

### 8.2 Человеческий стиль кода
- [ ] Пройтись по всем файлам — комментарии естественные:
  - `# форма на tochka-school грузится через js, без этого ожидания ловим stale element`
  - `# reqres отдаёт пустой {} на 404, проверяем именно статус`
  - `# маска телефона хитрая — сначала кликаем в поле, потом вводим цифры без +7`
- [ ] Убрать очевидные комментарии
- [ ] Имена переменных — естественные, не генеричные

### 8.3 Линтинг
- [ ] `ruff check . && ruff format .`
- [ ] Добавить ruff шаг в CI

### 8.4 Финальный ревью
- [ ] Нет хардкода секретов
- [ ] Все тесты независимы
- [ ] conftest.py на правильных уровнях
- [ ] `pytest tests/ -v` — всё зелёное
- [ ] `docker-compose up` — всё зелёное

### 8.5 Пуш
- [ ] `git push`
- [ ] CI зелёный на GitHub

---

## Бонус (после основных этапов)

### B.1 Расширение тестов
- [ ] Faker для рандомных данных API
- [ ] Проверка broken links на всех страницах
- [ ] `pytest-xdist` для параллельного запуска
- [ ] Responsive тесты (mobile/tablet/desktop viewport)

### B.2 Pre-commit hooks
- [ ] `.pre-commit-config.yaml` с ruff
- [ ] `pre-commit install`

### B.3 Мониторинг сайта
- [ ] Smoke-тест по cron в GitHub Actions (ежедневный прогон)
- [ ] Уведомления в Telegram при падении (бонус для работодателя)
