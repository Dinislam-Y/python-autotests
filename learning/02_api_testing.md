# API-тестирование — requests + pytest + Pydantic

> Все примеры — из реального кода проекта (reqres.in).
> Перед этим файлом прочитай [01_python_language.md](01_python_language.md)

---
---

## 1. requests — основы

### Dart (ты это знаешь):
```dart
final response = await http.get(Uri.parse('https://reqres.in/api/users/2'));
print(response.statusCode);  // 200
print(jsonDecode(response.body));
```

### Python:
```python
import requests

response = requests.get("https://reqres.in/api/users/2")
print(response.status_code)  # 200
print(response.json())       # сразу dict, без jsonDecode
```

### Все HTTP-методы
```python
requests.get(url)                          # получить
requests.post(url, json={"name": "Neo"})   # создать
requests.put(url, json={"name": "Neo"})    # заменить целиком
requests.patch(url, json={"job": "dev"})   # обновить частично
requests.delete(url)                       # удалить
```

### Сравнение
| Dart (`http`) | Python (`requests`) | Комментарий |
|---------------|---------------------|-------------|
| `http.get(Uri.parse(url))` | `requests.get(url)` | Не нужен `Uri.parse` |
| `await` обязателен | Синхронный по умолчанию | В тестах `await` не нужен |
| `jsonDecode(response.body)` | `response.json()` | Встроенный метод |
| `response.statusCode` | `response.status_code` | snake_case |
| `response.headers['content-type']` | `response.headers['content-type']` | Одинаково |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `json={"name": "Neo"}` | `data='{"name": "Neo"}'` | `json=` сам сериализует + ставит Content-Type |
| `params={"page": 2}` | Клеить URL руками: `url + "?page=2"` | `params` экранирует спецсимволы |
| `response.raise_for_status()` | Игнорировать status_code | Кинет исключение на 4xx/5xx |

### Где в проекте
`utils/api_client.py` — обёртка над requests. Каждый метод (`get`, `post`, ...) вызывает `self.session.get(url, **kwargs)` и логирует ответ.

---

## 2. Обработка ответов

### Response — что внутри

```python
response = requests.get("https://reqres.in/api/users/2")

response.status_code   # 200 — числовой код
response.json()        # dict — тело ответа, парсит JSON
response.text          # str — сырое тело (если не JSON)
response.headers       # dict — заголовки ответа
response.url           # str — финальный URL (после редиректов)
response.elapsed       # timedelta — время запроса
response.ok            # True если 200-299
```

### Проверка статуса в тестах

```python
# Наш паттерн (из user_checks.py):
assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"

# Или через ok:
assert response.ok, f"Запрос упал: {response.status_code}"
```

### Подводные камни
1. **`response.json()` на пустом теле** → `ValueError`. DELETE часто отдаёт 204 без тела — проверяй status_code, не парси JSON (см. `user_checks.py:44`)
2. **`response.text` всегда строка** — даже если тело пустое, вернёт `""`, не `None`
3. **Заголовки case-insensitive** — `response.headers["Content-Type"]` == `response.headers["content-type"]`

---

## 3. Session — переиспользование соединений

### Зачем
```python
# Без Session — каждый запрос = новое соединение
requests.get(url, headers={"x-api-key": key})   # соединение 1
requests.get(url2, headers={"x-api-key": key})  # соединение 2 — заново

# С Session — одно соединение на все запросы
session = requests.Session()
session.headers["x-api-key"] = key    # задал один раз
session.get(url)                      # переиспользует соединение
session.get(url2)                     # тот же сокет — быстрее
```

### Аналогия
Session — как вкладка в браузере. Открыл один раз, ходишь по страницам, куки и заголовки сохраняются. Без Session — каждый запрос = новый инкогнито-режим.

### Где в проекте
`utils/api_client.py:15` — `self.session = requests.Session()`. Один клиент на всю сессию тестов (scope="session" в фикстуре).

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `Session` + общие заголовки | `requests.get()` в каждом тесте | 100 тестов = 100 handshake'ов, медленно |
| Фикстура `scope="session"` для клиента | `scope="function"` | Новый клиент на каждый тест — бессмысленно |
| Закрывать сессию: `session.close()` | Оставить открытой | Утечка соединений |

---

## 4. Аутентификация

### Паттерны

```python
# 1. API-ключ в заголовке (наш проект, reqres.in)
session.headers["x-api-key"] = api_key

# 2. Bearer-токен
session.headers["Authorization"] = f"Bearer {token}"

# 3. Basic Auth
from requests.auth import HTTPBasicAuth
session.auth = HTTPBasicAuth("user", "password")

# 4. Куки
session.cookies.set("session_id", "abc123")
```

### Где хранить секреты

```
.env                          ← ключи, НЕ в git
config/config.py              ← Settings читает из .env
tests/api/conftest.py         ← фикстура передаёт ключ в ApiClient
```

```python
# config/config.py
class Settings(BaseSettings):
    api_key: str = ""          # из .env или пустой
    model_config = SettingsConfigDict(env_file=".env")

# tests/api/conftest.py
@pytest.fixture(scope="session")
def api_client(settings):
    return ApiClient(settings.base_url_api, api_key=settings.api_key)
```

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Ключи в `.env` | Хардкод в коде | Утечка в git → доступ к API |
| `.env` в `.gitignore` | Коммитить `.env` | Ключи в публичном репо |
| `.env.example` без значений | Нет примера | Новый разработчик не знает что заполнять |

---

## 5. pytest — фикстуры

### Ассоциация
Фикстура — **курьер пиццы**. Тест заказывает "мне api_client" — pytest смотрит в conftest, находит фикстуру с таким именем, "доставляет" готовый объект. Тест не знает как пицца готовилась.

### Как работает

```python
# conftest.py — "кухня"
@pytest.fixture(scope="session")
def api_client(settings):                    # settings — тоже фикстура!
    return ApiClient(settings.base_url_api, api_key=settings.api_key)  # готовим объект

# test_users.py — "клиент"
def test_get_user(self, api_client):          # pytest подставляет по имени
    response = api_client.get("/api/users/2")
```

### scope — время жизни

| scope | Когда создаётся заново | Аналогия | Пример |
|-------|----------------------|----------|--------|
| `function` | Каждый тест | Одноразовая тарелка | `user_checks` — дешёвый объект |
| `class` | Каждый тест-класс | Тарелка на стол | — |
| `module` | Каждый файл | Тарелка на кухню | — |
| `session` | Один раз на все тесты | Тарелка из фарфора | `api_client` — дорогое соединение |

### yield — setup + teardown в одном

```python
@pytest.fixture
def browser():
    driver = Chrome()          # setup (до yield)
    yield driver               # отдаём тесту
    driver.quit()              # teardown (после yield, ВСЕГДА)
```

### Цепочка фикстур в нашем проекте

```
test_get_single_user(self, api_client, user_checks)
                           │              │
         tests/api/conftest.py    tests/api/conftest.py
         api_client(settings)     user_checks()
                │                      │
      tests/conftest.py          return UserChecks()
      settings()
         │
   config/config.py
   settings = Settings()    ← читает .env
```

### Подводные камни
1. **Имя аргумента = имя фикстуры** — `def test(api_client):` ищет `@pytest.fixture` с именем `api_client`. Опечатка → `fixture not found`
2. **scope мismatch** — фикстура `scope="function"` не может зависеть от `scope="session"`. Наоборот — можно
3. **Не вызывай фикстуру руками** — `api_client()` в тесте = ошибка. Pytest сам вызывает и передаёт результат

---

## 6. pytest — параметризация

### Ассоциация
Связка ключей — один замок (тест), несколько ключей (данные). Вместо 3 копий теста — один тест, 3 прогона.

### Синтаксис

```python
# Простая — один параметр
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(user_id):
    response = api.get(f"/api/users/{user_id}")
    assert response.status_code == 200
# pytest создаст: test_get_user[1], test_get_user[2], test_get_user[3]

# Несколько параметров
@pytest.mark.parametrize("email, password, expected", [
    ("eve.holt@reqres.in", "pistol", 200),
    ("", "pistol", 400),
    ("eve.holt@reqres.in", "", 400),
])
def test_login(email, password, expected):
    response = api.post("/api/login", json={"email": email, "password": password})
    assert response.status_code == expected
```

### Где в проекте
`tests/api/test_resources.py` — `@pytest.mark.parametrize("resource_id", [1, 2, 3])`

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Имя в строке = имя аргумента | `@parametrize("id", ...)` но `def test(user_id):` | Тест не запустится |
| `parametrize` (без второго "e") | `parameterize` | Декоратор молча не сработает |
| ids для читаемости: `ids=["valid", "no_pass", "no_email"]` | Без ids | В отчёте: `test[param0]` вместо `test[valid]` |

---

## 7. pytest — хуки

### Что это
Хуки — точки входа в жизненный цикл pytest. Можно вмешаться в любой момент: до/после теста, при падении, при сборке отчёта.

### Часто используемые

```python
# conftest.py

# Скриншот при падении теста (для UI)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        # сделать скриншот, прикрепить к allure
        pass

# Добавить информацию в отчёт
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: дымовые тесты")

# Пропустить тесты по условию
def pytest_collection_modifyitems(items):
    for item in items:
        if "ui" in item.nodeid:
            item.add_marker(pytest.mark.skip("UI ещё не готов"))
```

### Аналогия
Хуки — как **перехватчики в CI/CD pipeline**. `before_script`, `after_script`, `on_failure` — только для тестов.

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Хуки в `conftest.py` | В тестовых файлах | Pytest может не найти |
| `hookwrapper=True` для "до + после" | Два отдельных хука | Сложнее поддерживать |
| Минимум логики в хуках | Тяжёлые операции | Замедлит каждый тест |

---

## 8. Pydantic — валидация ответов

### Зачем
Проверяем не только status_code, но и **структуру** ответа. Если API поменяет формат — тест упадёт на парсинге, а не молча пропустит.

### Dart (ты это знаешь):
```dart
class UserData {
  final int id;
  final String email;
  UserData.fromJson(Map<String, dynamic> json)
    : id = json['id'], email = json['email'];
}
```

### Python (Pydantic):
```python
from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

# Валидация:
user = UserData.model_validate(response.json())
# если id будет строкой → ValidationError
# если email отсутствует → ValidationError
```

### Паттерн из проекта

```python
# models.py — описал структуру
class SingleUserResponse(BaseModel):
    data: UserData          # вложенная модель
    support: Support

# user_checks.py — используешь в проверках
def check_user_found(self, response, user_id):
    assert response.status_code == 200
    user = SingleUserResponse.model_validate(response.json())  # парсинг + валидация
    assert user.data.id == user_id                             # доступ через точку
```

### Сравнение
| Dart (`fromJson`) | Python (Pydantic) | Комментарий |
|-------------------|-------------------|-------------|
| Руками: `json['id']` | Автоматически по type hints | Pydantic сам маппит |
| `if (json['id'] == null) throw` | `ValidationError` автоматически | Не нужны ручные проверки |
| `freezed` + `json_serializable` | `BaseModel` | Одна библиотека вместо двух |
| Compile-time проверка | Runtime проверка | Pydantic ловит ошибки при запуске |

### Опциональные поля

```python
class UpdateUserResponse(BaseModel):
    name: str = ""       # дефолт — PATCH может не вернуть name
    job: str
    updatedAt: str
```

### Подводные камни
1. **`model_validate` (v2)** не **`parse_obj` (v1)** — Pydantic 2 поменял API. В нашем проекте v2
2. **Pydantic конвертирует типы** — `{"id": "123"}` → `id = 123` (int). Это может скрыть баг API. Для строгости: `model_config = ConfigDict(strict=True)`
3. **Вложенные модели** — `data: UserData` → Pydantic рекурсивно валидирует

---

## 9. Allure-отчёты

### Декораторы — структура отчёта

```python
@allure.feature("Users API")                    # верхний уровень группировки
class TestUsers:

    @allure.story("Создание пользователя")      # подгруппа
    @allure.title("Создать юзера с именем")     # название теста в отчёте
    @allure.severity(allure.severity_level.CRITICAL)  # критичность
    def test_create_user(self, api_client):
        ...
```

### Шаги — что происходит внутри теста

```python
# user_checks.py
@allure.step("Проверка: пользователь найден (id={user_id})")
def check_user_found(self, response, user_id):
    assert response.status_code == 200
    ...
```

В отчёте: тест → развернул → видишь шаги с параметрами.

### Вложения — лог запроса

```python
# api_client.py
allure.attach(
    body=json.dumps(response.json(), indent=2),
    name=f"GET {url}",
    attachment_type=allure.attachment_type.JSON
)
```

### Иерархия в отчёте

```
Users API  (feature)
├── Получение пользователя  (story)
│   ├── Получить существующего по id  (title)
│   │   └── Проверка: пользователь найден (id=2)  (step)
│   └── Пользователь не найден — 404
└── Создание пользователя
    └── Создать пользователя с именем и должностью
```

### Запуск

```bash
pytest --alluredir=allure-results    # собрать данные
allure serve allure-results          # открыть отчёт в браузере
```

---

## 10. Тестовые данные

### Принцип
Данные отдельно от тестов. Тест — **сценарий** ("создай юзера и проверь"), данные — **входные параметры** ("имя = morpheus, должность = leader").

### Паттерн из проекта

```python
# test_data.py — константы
EXISTING_USER_ID = 2
VALID_EMAIL = "eve.holt@reqres.in"
CREATE_USER_NAME = "morpheus"

# test_users.py — только флоу
from tests.api.test_data import CREATE_USER_NAME, CREATE_USER_JOB

def test_create_user(self, api_client, user_checks):
    response = api_client.post("/api/users", json={
        "name": CREATE_USER_NAME,
        "job": CREATE_USER_JOB
    })
    user_checks.check_user_created(response, CREATE_USER_NAME, CREATE_USER_JOB)
```

### Faker — случайные данные

```python
# utils/helpers.py
from faker import Faker
fake = Faker("ru_RU")

def random_user():
    return {"name": fake.first_name(), "job": fake.job()}

# В тесте:
from utils.helpers import random_user
data = random_user()  # {"name": "Алексей", "job": "Программист"}
```

### Когда что использовать

| Подход | Когда | Пример |
|--------|-------|--------|
| Константы в `test_data.py` | Фиксированные, API требует конкретные | `VALID_EMAIL` — reqres принимает только его |
| Faker | Произвольные данные | Имя юзера для POST — неважно какое |
| `.env` | Секреты | API-ключи, пароли |
| `@parametrize` | Множество вариантов | Список id для проверки |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `SCREAMING_CASE` для констант | `validEmail` (camelCase) | Не Python-стиль, спутают с переменной |
| Один `test_data.py` на модуль | Хардкод в тестах | Данные размазаны, тяжело менять |
| Faker для "неважных" данных | Faker для всего | Тесты станут нестабильными |

---

## 11. Конфигурация — pydantic-settings

### Зачем
Один класс `Settings` — все настройки проекта. Читает из `.env`, есть дефолты, type-safe.

### Как работает

```python
# config/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_url_api: str = "https://reqres.in"       # дефолт
    api_key: str = ""                              # из .env
    headless: bool = True                          # для Playwright
    timeout: int = 30000

    model_config = SettingsConfigDict(
        env_file=".env",                           # откуда читать
        env_file_encoding="utf-8",
    )

settings = Settings()   # синглтон
```

```bash
# .env
API_KEY=pro_d2f08ff9...
HEADLESS=false           # переопределяет дефолт
```

### Приоритет значений
1. Переменные окружения (CI/CD) — высший
2. `.env` файл — средний
3. Дефолт в классе — низший

### Аналог в Dart
Dart: `dotenv` + ручной парсинг. Python: `pydantic-settings` делает всё — парсит, конвертирует типы, валидирует.

---

## 12. Моки

### Что это
Мок — подделка. Вместо реального сервера/API тест общается с "куклой", которая отвечает как настоящий.

### Когда мокать

| Мокай | Не мокай |
|-------|----------|
| Внешний API недоступен (платный, нестабильный) | Твой API — тестируй по-настоящему |
| Нужно проверить обработку ошибок (500, timeout) | Простые CRUD-операции |
| CI без доступа к сети | Интеграционные тесты |

### Простой пример

```python
from unittest.mock import patch, MagicMock

@patch("requests.Session.get")
def test_handles_server_error(mock_get):
    # настраиваем "куклу"
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal Server Error"}
    mock_get.return_value = mock_response

    # тест работает с "куклой" вместо реального API
    response = api_client.get("/api/users/1")
    assert response.status_code == 500
```

### Библиотеки

| Библиотека | Что делает | Когда |
|-----------|-----------|-------|
| `unittest.mock` | Встроенная, подменяет объекты | Базовые моки |
| `responses` | Мокает requests на уровне HTTP | API-тесты без сети |
| `pytest-mock` | Обёртка над unittest.mock для pytest | Удобнее синтаксис |

### Подводные камни
1. **Мок — не замена тестам** — мок проверяет твой код, не API. Если API поменяется — мок не узнает
2. **`@patch` путь** — мокаешь **откуда импортируется**, не где определён: `@patch("utils.api_client.requests")`, не `@patch("requests")`
3. **Чрезмерное мокирование** — если мокаешь всё, тест проверяет сам себя. Бессмысленно

---

## 13. Хороший автотест — чеклист

### Критерии

| Критерий | Что значит | Антипаттерн |
|----------|-----------|-------------|
| **Независимый** | Не зависит от других тестов, порядка запуска | Тест B падает если не запустить A |
| **Повторяемый** | Одинаковый результат при повторном запуске | Зависит от времени, рандома, состояния БД |
| **Быстрый** | API-тест < 5 сек, UI < 30 сек | Тест ждёт 60 сек "на всякий случай" |
| **Читаемый** | По названию понятно что проверяет | `test_1`, `test_case_42` |
| **Один assert** | Проверяет одну вещь (логически) | 10 assert в одном тесте — упал первый, остальные не узнаешь |
| **Без if/else** | Тест — сценарий, не программа | `if status == 200: ... else: ...` в тесте |

### Наш паттерн — 3 слоя

```
Тест (флоу)           →  test_users.py      — только вызовы
  ↓
Действие (запрос)     →  api_client.py       — отправляет запрос
  ↓
Проверка (assert)     →  user_checks.py      — проверяет ответ
```

Тест-файл **не содержит**: селекторы, assert, if/else, хардкод данных.

### Именование

```python
# Хорошо — понятно что проверяет:
def test_create_user_with_name_and_job(self):
def test_user_not_found_returns_404(self):
def test_register_without_password_fails(self):

# Плохо — что это?:
def test_1(self):
def test_user(self):
def test_api(self):
```

---

## 14. Параллелизация тестов

### Зачем
100 тестов по 2 сек = 200 сек. С 4 воркерами = ~50 сек.

### pytest-xdist

```bash
pip install pytest-xdist
pytest -n 4              # 4 параллельных воркера
pytest -n auto           # по числу ядер CPU
```

### Требования к тестам

| Требование | Почему | Что сломается |
|-----------|--------|---------------|
| Независимые тесты | Параллельно = случайный порядок | Тест B ждёт данные от A |
| Нет общего состояния | Два теста пишут в одну БД | Гонка данных |
| Уникальные данные | Два теста создают `user@test.com` | Конфликт уникальности |
| `scope="session"` осторожно | Фикстура создаётся **в каждом воркере** | 4 воркера = 4 браузера |

### Подводные камни
1. **`scope="session"` + xdist** — каждый воркер создаёт свою сессионную фикстуру. Для общей на всех — `pytest-xdist` группы или `tmp_path_factory`
2. **Порядок тестов** — с xdist порядок случайный. Если тесты зависят друг от друга — сначала исправь, потом параллель
3. **Логи перемешаются** — используй `--tb=short` и Allure для читаемых отчётов

---

## 15. Лучшие практики — итого

### Структура API-тестов

```
tests/api/
├── conftest.py          ← фикстуры: api_client, user_checks
├── test_data.py         ← константы: EXISTING_USER_ID, VALID_EMAIL
├── models.py            ← Pydantic-модели ответов
├── checks/
│   ├── user_checks.py   ← проверки для /users
│   └── auth_checks.py   ← проверки для /register, /login
├── test_users.py        ← CRUD тесты
├── test_register.py     ← auth тесты
└── test_resources.py    ← параметризованные тесты
```

### Антипаттерны

| Антипаттерн | Почему плохо | Как правильно |
|------------|-------------|---------------|
| `assert` прямо в тесте | Нечитаемо, не переиспользуется | Check-классы с `@allure.step` |
| Хардкод URL в тесте | Сменил стенд = правишь 50 тестов | `config.py` + `.env` |
| `time.sleep(5)` | Медленно и ненадёжно | Для API — не нужно, запрос синхронный |
| Один гигантский `conftest.py` | Невозможно разобраться | Conftest на каждый уровень |
| Тест зависит от другого теста | Падает каскадом | Каждый тест — самостоятельный |

---
---

# НАВИГАЦИЯ

| Файл | Что внутри |
|------|-----------|
| [00 — Шпаргалка для собеса](00_interview_cheatsheet.md) | Определения + подвох-вопросы |
| [01 — Python язык](01_python_language.md) | Подробный разбор с Dart-мостиком |
| **02 — API-тестирование** | **Ты здесь** |
| [03 — UI-тестирование](03_ui_testing.md) | Playwright Python |
