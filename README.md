# Python QA Autotests

[![CI](https://github.com/Dinislam-Y/python-autotests/actions/workflows/tests.yml/badge.svg)](https://github.com/Dinislam-Y/python-autotests/actions)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Tests](https://img.shields.io/badge/tests-44%20passed-brightgreen)

Автотесты для лендинга **Точка Знаний** (UI) и **reqres.in** (API).

Проект вырос из моего опыта в Flutter QA — я адаптировал архитектуру, которую обкатал на 4000+ тестах, под Python-стек. Здесь тот же принцип строгого разделения ответственности, только вместо Flutter-виджетов — Playwright и requests.

---

## Стек

| Категория | Инструмент | Зачем |
|-----------|-----------|-------|
| Фреймворк | pytest | Гибкие фикстуры, маркеры, параметризация |
| UI | Playwright | Быстрый, стабильный, авто-ожидания |
| API | requests + Pydantic | HTTP-запросы + валидация схемы ответов |
| Отчёты | Allure | Steps, скриншоты при падении, история |
| Линтер | ruff | Быстрый, заменяет flake8+isort+black |
| CI/CD | GitHub Actions | Прогон на пуше, деплой Allure на Pages |
| Контейнер | Docker | Воспроизводимый запуск одной командой |

## Архитектура

Я перенёс из Flutter трёхслойный паттерн **Locators → Pages → Checks**. В моём опыте это единственная схема, которая нормально масштабируется и выдерживает мутационное тестирование:

```
Locators   — только селекторы, никакой логики
Pages      — только действия (click, fill, navigate), никаких assert
Checks     — только проверки (assert), каждый метод — одно условие
Tests      — только флоу: page.action() + check.verify(), без if/else
```

Тест выглядит так:

```python
def test_main_page_opens(main_page, main_page_checks):
    main_page.open()
    main_page_checks.check_title_contains("Точка")
    main_page_checks.check_hero_banner_visible()
```

Никаких селекторов в тестах, никаких ассертов в страницах. Если тест падает — сразу ясно, где проблема: в локаторе, в действии или в проверке.

## Структура проекта

```
python-autotests/
├── tests/
│   ├── conftest.py                     # Общие фикстуры (settings)
│   ├── api/
│   │   ├── conftest.py                 # API-фикстуры (api_client)
│   │   ├── test_data.py                # Константы — как Dependencies во Flutter
│   │   ├── models.py                   # Pydantic-модели ответов
│   │   ├── checks/                     # Ассерты: user_checks, auth_checks
│   │   ├── test_users.py               # CRUD users (7 тестов)
│   │   ├── test_register.py            # Регистрация/логин (4 теста)
│   │   └── test_resources.py           # Ресурсы + параметризация (6 тестов)
│   └── ui/
│       ├── conftest.py                 # UI-фикстуры, скриншот при падении
│       ├── test_data.py                # URL разделов, ожидаемые тексты
│       ├── locators/                   # Селекторы: header, main, courses, form, footer
│       ├── pages/                      # Page Objects (только действия)
│       ├── checks/                     # Проверки (только assert)
│       ├── test_navigation.py          # Навигация по разделам (12 тестов)
│       ├── test_main_page.py           # Главная страница (4 теста)
│       ├── test_courses.py             # Каталог курсов (5 тестов)
│       ├── test_enrollment_form.py     # Форма записи (3 теста)
│       └── test_footer.py             # Футер и ссылки (3 теста)
├── utils/
│   ├── api_client.py                   # HTTP-обёртка с Allure-вложениями
│   └── helpers.py                      # Faker для тестовых данных
├── config/
│   ├── config.py                       # Pydantic Settings (.env)
│   └── .env.example                    # Шаблон переменных окружения
├── Dockerfile                          # Python + Playwright + браузеры
├── docker-compose.yml                  # Запуск тестов одной командой
├── .dockerignore
└── pyproject.toml                      # Зависимости, pytest, ruff
```

---

## Быстрый старт

### 1. Клонирование и установка

```bash
git clone https://github.com/Dinislam-Y/python-autotests.git
cd python-autotests

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
playwright install chromium
```

### 2. Настройка API-ключа

reqres.in требует бесплатный API-ключ ([получить тут](https://app.reqres.in/signup)):

```bash
cp config/.env.example .env
# открыть .env и вставить свой ключ в API_KEY=...
```

### 3. Запуск тестов

```bash
# все тесты (API + UI)
pytest

# только API
pytest -m api

# только UI (headless — без браузера)
pytest -m ui

# UI с браузером — видно что происходит
pytest -m ui --headed

# UI замедленный — 1 сек между действиями, удобно смотреть
pytest -m ui --headed --slowmo=1000

# smoke-набор (самые важные)
pytest -m smoke

# конкретный файл
pytest tests/ui/test_navigation.py -v --headed

# конкретный тест
pytest tests/ui/test_navigation.py::TestNavigation::test_main_page_opens -v --headed
```

---

## Запуск в Docker

Docker позволяет запустить тесты без установки Python, Playwright и браузеров — всё внутри контейнера.

### Через docker compose (рекомендуется)

```bash
# собрать образ и запустить тесты
docker compose up --build

# результаты Allure появятся в ./allure-results/ на хосте
allure serve allure-results
```

### Через docker напрямую

```bash
# собрать образ
docker build -t python-autotests .

# запустить тесты
docker run --env-file .env -v ./allure-results:/app/allure-results python-autotests

# запустить только API тесты
docker run --env-file .env python-autotests pytest tests/api/ -v

# запустить только UI
docker run --env-file .env -v ./allure-results:/app/allure-results python-autotests pytest tests/ui/ -v
```

### Важно

- Docker Desktop должен быть запущен
- `.env` файл с `API_KEY` нужен для API тестов
- `--headed` в Docker не работает (нет монитора), только headless
- Allure-результаты пробрасываются через volume на хост

---

## Allure-отчёт

Отчёт генерируется автоматически при каждом прогоне (`--alluredir=allure-results` в pyproject.toml).

```bash
# установка allure CLI (один раз)
brew install allure

# открыть отчёт в браузере (запускает локальный сервер)
allure serve allure-results

# сгенерировать статический HTML-отчёт
allure generate allure-results -o allure-report --clean
open allure-report/index.html
```

Что увидишь в отчёте:
- **Features** — группировка по модулям (Users API, Навигация, Каталог курсов...)
- **Stories** — сценарии внутри модулей
- **Steps** — каждый шаг теста (открытие страницы, клик, проверка)
- **Attachments** — JSON-ответы API, скриншоты при падении UI тестов

На CI отчёт автоматически публикуется на **GitHub Pages** после каждого прогона.

---

## Покрытие тестами

| Сьют | Тестов | Что проверяем |
|------|--------|---------------|
| API: Users | 7 | GET/POST/PUT/PATCH/DELETE /api/users |
| API: Auth | 4 | Регистрация и логин (позитив + негатив) |
| API: Resources | 6 | Параметризация по id и пагинации |
| UI: Навигация | 12 | Все разделы, возрастные категории, логотип |
| UI: Главная | 4 | Баннер, категории, направления, отзывы |
| UI: Курсы | 5 | Каталог, карточки, страницы предметов |
| UI: Форма | 3 | Модалка, поле телефона, кнопка записи |
| UI: Футер | 3 | Соцсети, документы, лицензия |
| **Итого** | **44** | |
