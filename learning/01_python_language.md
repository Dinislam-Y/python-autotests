# Python для Dart-разработчика

> Мостик между языками. Не учебник с нуля, а справочник отличий.
> Читай по порядку первый раз, потом используй как шпаргалку.
>
> Подробные вопросы-ответы — в [NOTES.md](../NOTES.md)

---

## 0. Сдвиг мышления

В Dart ты привык: компилятор ловит ошибки типов, фигурные скобки — структура, `final` защищает от перезаписи.

В Python всё держится на **договорённостях между людьми**, а не на запретах компилятора:
- `SCREAMING_CASE` = "не трогай" — но язык не помешает изменить
- Отступы = структура — не стиль, а синтаксис
- Duck typing: "если ходит как утка и крякает — значит утка"

```python
# Zen of Python (import this) — 3 главных правила:
# 1. Explicit is better than implicit — явное лучше неявного
# 2. Readability counts — читаемость имеет значение
# 3. There should be one obvious way to do it — один очевидный способ
```

| Dart | Python | Суть |
|------|--------|------|
| Компилятор защищает | Конвенции защищают | `final` vs `UPPER_CASE` — один запрещает, другой просит |
| Nominal typing: тип = класс | Duck typing: тип = поведение | Если у объекта есть `.read()` — он "файл", неважно какой класс |
| `dynamic` — opt-out из типов | Типы — opt-in (`type hints`) | По умолчанию всё "динамическое", type hints добавляешь сам |

---

## 1. Окружение и инструменты

### Dart (ты это знаешь):
```yaml
# pubspec.yaml
name: my_app
dependencies:
  http: ^1.2.0
dev_dependencies:
  test: ^1.25.0
```
```bash
dart pub get        # установить зависимости
dart test           # запустить тесты
```

### Python:
```toml
# pyproject.toml
[project]
name = "python-autotests"
requires-python = ">=3.9"
dependencies = [
    "pytest>=8.0",
    "requests",
]
[project.optional-dependencies]
dev = ["ruff"]
```
```bash
python -m venv .venv        # создать виртуальное окружение
source .venv/bin/activate   # активировать (macOS/Linux)
pip install -e ".[dev]"     # установить зависимости
pytest                      # запустить тесты
```

### Ключевое отличие
В Dart пакеты глобальные (`.pub-cache`). В Python **каждый проект живёт в своём `venv`** — изолированная песочница. Без `venv` пакеты ставятся системно и конфликтуют между проектами.

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `pubspec.yaml` | `pyproject.toml` | Формат другой, суть та же |
| `pub get` | `pip install -e .` | `-e` = editable, как `pub get` в dev-режиме |
| `pub add http` | `pip install requests` | Но в Python ещё надо добавить в pyproject.toml руками |
| `.pub-cache` (глобально) | `.venv/` (в каждом проекте) | Главное отличие — изоляция |
| `dart test` | `pytest` | pytest мощнее чем `dart test` |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Всегда работай в `venv` | `pip install` без venv | Пакеты засорят системный Python, конфликты версий |
| Фиксируй версии: `pytest>=8.0` | `pytest` без версии | Через полгода поставится pytest 9.x и тесты сломаются |
| `.venv/` в `.gitignore` | Коммитить `.venv/` | 200+ МБ мусора в репо |

### Попробуй
Открой `pyproject.toml` в проекте. Найди:
1. Аналог секции `dependencies` из pubspec
2. Аналог `dev_dependencies`
3. Где настроены маркеры pytest (как `tags` в `dart test`)

---

## 2. Синтаксис: отличия от Dart

### Dart (ты это знаешь):
```dart
void greet(String name) {
  if (name.isNotEmpty) {
    print('Hello, $name!');
  } else {
    print('No name');
  }
}
```

### Python:
```python
def greet(name: str):
    if name:                    # пустая строка = False (truthiness)
        print(f"Hello, {name}!")
    else:
        print("No name")
```

### Ключевое отличие
Отступы — это синтаксис. Забыл отступ → `IndentationError`. Поставил лишний → `IndentationError`. Dart прощает форматирование, Python — нет.

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `{}` для блоков | Отступы (4 пробела) | Табы тоже работают, но смешивать нельзя |
| `null` | `None` | Одно и то же, разное имя |
| `true` / `false` | `True` / `False` | С большой буквы! |
| `;` в конце строки | Ничего | Точку с запятой можно поставить, но зачем |
| `//` комментарий | `#` комментарий | `///` doc → `"""` docstring |
| Нет аналога | `pass` | Заглушка для пустого блока |
| `is` проверка типа | `isinstance()` | `is` в Python — сравнение identity (==, не ===) |
| `?.` null-safe | Нет встроенного | В Python: `x if x is not None else default` или `getattr()` |
| `??` null-coalescing | `or` / `if-else` | `name or "default"` — но осторожно с `0` и `""` |

### Операторы

| Dart | Python | Комментарий |
|------|--------|-------------|
| `+`, `-`, `*`, `/` | `+`, `-`, `*`, `/` | Одинаково. `/` всегда возвращает `float`! |
| `~/` (целочисленное) | `//` | `7 // 2` → `3`. В Dart: `7 ~/ 2` → `3` |
| `%` (остаток) | `%` | Одинаково |
| Нет аналога | `**` (степень) | `2 ** 10` → `1024`. В Dart: `pow(2, 10)` |
| `&&` | `and` | Слово вместо символа |
| `\|\|` | `or` | Слово вместо символа |
| `!` | `not` | Слово вместо символа |
| `==`, `!=` | `==`, `!=` | Одинаково (сравнение значений) |
| `>`, `<`, `>=`, `<=` | `>`, `<`, `>=`, `<=` | Одинаково |
| `identical(a, b)` | `a is b` | Сравнение identity (один объект в памяти) |
| `is` (проверка типа) | `isinstance(x, int)` | В Python `is` — identity, не тип! |
| `as` (приведение) | Нет — duck typing | Python не приводит типы явно |
| `??` | `or` (осторожно!) | `name or "default"` — но `0 or "default"` → `"default"` |
| `??=` | `x = x or default` | Или `if x is None: x = default` |

```python
# Логические операторы — слова, не символы:
if name and age > 18:          # Dart: if (name != null && age > 18)
if not is_blocked or is_admin:  # Dart: if (!isBlocked || isAdmin)

# Короткое замыкание (short-circuit) — как в Dart:
result = name or "Anonymous"    # если name falsy → "Anonymous"
result = items and items[0]     # если items пустой → не обращается к items[0]
```

### Циклы

```python
# for — перебор коллекции (как for-in в Dart)
for user in users:
    print(user.name)

# for с индексом
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 3): # 2, 5, 8  (старт, стоп, шаг)
    print(i)

# while
count = 0
while count < 5:
    print(count)
    count += 1             # Python нет ++ и --!

# break — выйти из цикла
for item in items:
    if item.is_target:
        result = item
        break              # нашёл — выходим

# continue — пропустить итерацию
for user in users:
    if user.is_blocked:
        continue           # пропускаем заблокированных
    process(user)

# else в цикле (нет в Dart!) — выполнится если цикл НЕ прервался break'ом
for user in users:
    if user.is_admin:
        break
else:
    print("Админов нет")   # выполнится только если break не сработал
```

| Dart | Python | Комментарий |
|------|--------|-------------|
| `for (var i = 0; i < n; i++)` | `for i in range(n):` | `range` вместо счётчика |
| `for (var item in list)` | `for item in list:` | Почти идентично |
| `list.forEach((e) => ...)` | `for e in list:` | В Python нет `forEach` |
| `i++` / `i--` | `i += 1` / `i -= 1` | `++`/`--` не существуют в Python |
| `do { } while (cond)` | Нет аналога | Используй `while True: ... if cond: break` |
| Нет аналога | `for...else` | Блок `else` после `for` — уникальная фича Python |

### Truthiness — то чего нет в Dart
Python считает "пустое" = `False`:

| Значение | bool() | Dart аналог |
|----------|--------|-------------|
| `""` | `False` | `"".isEmpty == true` |
| `0`, `0.0` | `False` | Нет аналога — `0` это просто число |
| `[]`, `{}`, `set()` | `False` | `[].isEmpty == true` |
| `None` | `False` | `null == null` |
| Всё остальное | `True` | — |

Это используется в тестах: `assert user.id` — проверяет что id не пустой (см. NOTES.md #8).

### Подводные камни
1. **Смешал табы и пробелы** → `TabError`. IDE обычно спасает, но если копируешь код из интернета — проверь
2. **Написал `if name == True`** вместо `if name:` → строка `"hello"` это не `True`, тест упадёт
3. **Забыл `:`** после `if`, `def`, `class`, `for` → `SyntaxError`. В Dart `{` заменяет эту роль

### Попробуй
Открой `tests/api/checks/user_checks.py:33`. Найди `assert user.id` — это truthiness-проверка. Что будет если `id = 0`? А если `id = ""`?

---

## 3. Типы данных и коллекции

### Dart (ты это знаешь):
```dart
final List<String> names = ['Alice', 'Bob'];
final Map<String, int> scores = {'Alice': 95, 'Bob': 87};
final Set<int> unique = {1, 2, 3};
// Dart не имеет tuple
```

### Python:
```python
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
unique: set[int] = {1, 2, 3}
point: tuple[int, int] = (10, 20)  # неизменяемый! Dart аналога нет
```

### Сравнение коллекций
| Dart | Python | Мутабельный? | Комментарий |
|------|--------|-------------|-------------|
| `List<T>` | `list[T]` | Да | Почти одинаковы |
| `Map<K, V>` | `dict[K, V]` | Да | Python `dict` хранит порядок вставки (3.7+) |
| `Set<T>` | `set[T]` | Да | Идентичны |
| Нет аналога | `tuple[T, ...]` | **Нет** | Как `const List`, но ещё и хешируемый |
| `const [1, 2]` | `(1, 2)` | **Нет** | tuple — главная замена Dart `const` коллекций |
| Нет аналога | `frozenset({1, 2})` | **Нет** | Неизменяемый set — можно использовать как ключ dict |
| `Object?` | `Any` / `None` | — | `None` вместо `null` |

### Операции — мостик
| Dart | Python | Что делает |
|------|--------|-----------|
| `list.add(x)` | `list.append(x)` | Добавить элемент |
| `list.addAll([1,2])` | `list.extend([1,2])` или `list += [1,2]` | Добавить несколько |
| `list.contains(x)` | `x in list` | Проверка наличия |
| `list.length` | `len(list)` | Длина — функция, не свойство! |
| `list.where((e) => ...)` | `[e for e in list if ...]` | Фильтрация (comprehension, глава 6) |
| `list.map((e) => ...)` | `[f(e) for e in list]` | Маппинг |
| `map['key']` | `dict['key']` | Доступ. KeyError если нет ключа! |
| `map['key'] ?? default` | `dict.get('key', default)` | Безопасный доступ |
| `map.containsKey(k)` | `k in dict` | Проверка ключа |
| `map.entries` | `dict.items()` | Пары ключ-значение |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `dict.get("key", default)` | `dict["key"]` без проверки | `KeyError` в рантайме |
| `x in my_list` | `my_list.count(x) > 0` | `count` проходит весь список — O(n) всегда |
| `tuple` для неизменяемых данных | `list` для констант | Случайно изменишь и не заметишь |
| `set` для поиска уникальных | `list` + проверка дубликатов | `set` ищет за O(1), `list` за O(n) |

### Подводные камни
1. **`dict["missing_key"]`** → `KeyError`, не `null`. Dart `map['x']` вернёт `null`. Python падает. Используй `.get()`
2. **Мутабельность по умолчанию** — `list`, `dict`, `set` мутабельны. Если передал в функцию — она может изменить оригинал. В Dart `List` тоже, но Dart приучает к `final`/`const`
3. **Пустой `set`** — `{}` это пустой `dict`, не `set`! Пустой set = `set()`

### Попробуй
Открой `tests/api/models.py`. Найди `data: list[UserData]` (строка 31) — это type hint для списка Pydantic-моделей. Как бы это выглядело в Dart?

---

## 4. Строки и форматирование

### Dart (ты это знаешь):
```dart
final name = 'Morpheus';
final url = '/api/users/$userId';
final msg = 'Hello, ${user.name}!';
final multi = '''
  Многострочная
  строка
''';
```

### Python:
```python
name = "Morpheus"
url = f"/api/users/{user_id}"          # f-string — аналог Dart $
msg = f"Hello, {user.name}!"
multi = """
  Многострочная
  строка
"""
```

### Ключевое отличие
Dart: `$variable` и `${expression}`. Python: `{variable}` и `{expression}` — но только внутри f-строки (с буквой `f` перед кавычками). Забыл `f` → получишь буквальный текст `{variable}`.

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `'$name'` | `f"{name}"` | Не забудь `f` перед кавычкой |
| `'${obj.field}'` | `f"{obj.field}"` | Одинаково, только `$` → `{}` |
| `'''multiline'''` | `"""multiline"""` | Тройные кавычки — идентично |
| `r'\no\escaping'` | `r"\no\escaping"` | Raw strings — одинаково |
| `'Hello' + ' ' + name` | `f"Hello {name}"` | Конкатенация работает, но f-string чище |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `f"/api/users/{id}"` | `"/api/users/" + str(id)` | Работает, но нечитаемо |
| `f"Ожидал {expected}, получил {actual}"` | `"Ожидал " + str(expected)` | assert-сообщения должны быть читаемыми |
| `f"{value!r}"` для дебага | `f"{value}"` | `!r` добавляет кавычки: `'hello'` вместо `hello` |

### Подводные камни
1. **Забыл `f`** → `"{name}"` вернёт буквально текст `{name}`, без подстановки. Dart не даст забыть `$`
2. **f-string с `\n` внутри `{}`** → `SyntaxError`. Внутри `{}` нельзя ставить backslash
3. **`.format()` метод** — старый способ: `"Hello, {}".format(name)`. Встретишь в чужом коде, но сам используй f-strings

### Попробуй
Открой `utils/api_client.py:21`. Найди f-string `f"{self.base_url}{path}"`. Как бы ты написал это в Dart?

---

## 5. Функции

### Dart (ты это знаешь):
```dart
// именованные параметры
void createUser({required String name, String job = "tester"}) { ... }
createUser(name: "Neo", job: "developer");

// стрелочная функция
int double(int x) => x * 2;
```

### Python:
```python
# позиционные + дефолтные
def create_user(name: str, job: str = "tester"): ...
create_user("Neo", job="developer")  # job можно по имени

# *args — произвольное число позиционных
def log(*messages):
    for msg in messages:
        print(msg)
log("hello", "world", "!")

# **kwargs — произвольное число именованных
def get(self, path: str, **kwargs) -> Response:
    return self.session.get(url, **kwargs)
# вызов: api.get("/users", params={"page": 2}, timeout=5)
# kwargs = {"params": {"page": 2}, "timeout": 5}

# lambda — анонимная функция (одно выражение)
sort_by_name = lambda user: user["name"]  # аналог (user) => user["name"]
```

### Ключевое отличие
В Dart именованные параметры (`{name}`) и позиционные — разные синтаксисы. В Python любой параметр можно передать и позиционно, и по имени. `**kwargs` — это как `Map<String, dynamic>` для "всего остального".

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `void fn()` | `def fn():` | `void` не нужен, можно добавить `-> None` |
| `int fn(int x)` | `def fn(x: int) -> int:` | Type hints опциональны, но мы их пишем |
| `{required String name}` | `name: str` (без дефолта) | В Python без дефолта = обязательный |
| `{String name = "x"}` | `name: str = "x"` | Дефолтные — одинаково |
| `(int x) => x * 2` | `lambda x: x * 2` | Lambda — одно выражение, без `return` |
| Нет аналога | `*args` | Все "лишние" позиционные → tuple |
| Нет аналога | `**kwargs` | Все "лишние" именованные → dict |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `def fn(items: list = None):` + `items = items or []` | `def fn(items: list = []):` | МУТАБЕЛЬНЫЙ ДЕФОЛТ — список расшарен между вызовами! |
| `def fn(*, name, age):` | Без `*` для keyword-only | `*` заставляет передавать по имени — читаемее |
| Type hints на всех параметрах | Без hints | Dart-привычка — сохрани её, IDE поможет |

### Scope — области видимости

```python
x = "global"                      # глобальная переменная

def outer():
    x = "outer"                    # локальная в outer

    def inner():
        # x = "inner"             # создаст НОВУЮ локальную, не изменит outer
        nonlocal x                 # "хочу менять переменную из outer"
        x = "changed by inner"

    inner()
    print(x)                       # "changed by inner"

outer()
print(x)                           # "global" — глобальная не тронута
```

| Dart | Python | Комментарий |
|------|--------|-------------|
| Лексическая область (как Python) | LEGB: Local → Enclosing → Global → Built-in | Порядок поиска переменных |
| Нет аналога | `global x` | Позволяет менять глобальную переменную из функции |
| Нет аналога | `nonlocal x` | Позволяет менять переменную из внешней функции |
| `final` запрещает перезапись | Нет аналога | Python позволяет всё, полагается на конвенции |

**LEGB** — порядок поиска переменной: **L**ocal (в функции) → **E**nclosing (во внешней функции) → **G**lobal (в модуле) → **B**uilt-in (`len`, `print`).

### GOTCHA: мутабельный дефолт
```python
# ОПАСНО! Список создаётся ОДИН РАЗ при определении функции
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"] ← сюрприз! тот же список!

# ПРАВИЛЬНО:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
В Dart такой проблемы нет — `const []` создаётся заново. В Python дефолт вычисляется один раз.

### Подводные камни
1. **Мутабельный дефолт** (см. выше) — самый коварный баг. Линтер ruff ловит это (правило `B006`)
2. **`return` без значения** → возвращает `None`, не вызывает ошибку. В Dart `void` явно говорит "ничего"
3. **Порядок**: `def fn(a, b=1, *args, **kwargs)` — дефолтные до `*args`, `**kwargs` последний

### Попробуй
Открой `utils/api_client.py:32`. Разбери метод `get(self, path, **kwargs)`:
1. Что попадёт в `kwargs` при вызове `api.get("/users", params={"page": 2})`?
2. Что делает `self.session.get(url, **kwargs)` — как `**` "распаковывает" dict?

---

## 6. Comprehensions

### Dart (ты это знаешь):
```dart
// фильтр + маппинг
final active = users.where((u) => u.isActive).map((u) => u.name).toList();

// генерация списка
final squares = List.generate(5, (i) => i * i);
```

### Python:
```python
# list comprehension — фильтр + маппинг в одну строку
active = [u.name for u in users if u.is_active]

# генерация
squares = [i * i for i in range(5)]

# dict comprehension
status_map = {u.id: u.status for u in users}

# set comprehension
unique_names = {u.name for u in users}
```

### Ключевое отличие
В Dart — цепочка методов (`.where().map().toList()`). В Python — одно выражение внутри `[]`/`{}`/`()`. Читается как предложение: "дай мне `u.name` для каждого `u` в `users`, если `u.is_active`".

### Сравнение
| Dart | Python | Результат |
|------|--------|----------|
| `list.where((e) => cond).toList()` | `[e for e in list if cond]` | Отфильтрованный list |
| `list.map((e) => f(e)).toList()` | `[f(e) for e in list]` | Преобразованный list |
| `Map.fromEntries(...)` | `{k: v for k, v in items}` | dict |
| `list.toSet()` | `{e for e in list}` или `set(list)` | set |
| `List.generate(n, (i) => ...)` | `[... for i in range(n)]` | Генерация по индексу |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `[x for x in items if x > 0]` | Вложенный `for` + `if` + `append` | Comprehension в 2-3x быстрее и читаемее |
| Разбей на переменные если > 1 строки | `[f(x) for x in [g(y) for y in items if h(y)] if p(x)]` | Нечитаемо. Лучше 2 строки |
| Generator `(x for x in big_list)` для больших данных | `[x for x in million_items]` | List создаёт всё в памяти, generator — лениво |

### Подводные камни
1. **`{}`** без `:` — это `set`, не `dict`! `{x for x in items}` → set. `{x: y for ...}` → dict
2. **Утечка переменной** — в Python 2 `x` утекала из comprehension. В Python 3 — нет, но в обычном `for` — да

### Попробуй
Перепиши это Dart-выражение в Python comprehension:
```dart
final ids = users.where((u) => u.status == 200).map((u) => u.id).toList();
```

---

## 7. ООП — главная глава

### Dart (ты это знаешь):
```dart
class ApiClient {
  final String baseUrl;

  ApiClient(this.baseUrl);           // конструктор

  String get fullUrl => baseUrl;     // геттер

  Future<Response> get(String path) async {
    return http.get(Uri.parse('$baseUrl$path'));
  }
}
```

### Python:
```python
class ApiClient:
    """Обёртка над requests.Session."""        # docstring вместо ///

    def __init__(self, base_url: str):         # конструктор = __init__
        self.base_url = base_url               # this.baseUrl → self.base_url

    @property
    def full_url(self) -> str:                 # геттер = @property
        return self.base_url

    def get(self, path: str) -> Response:      # self — ВСЕГДА первый аргумент
        return self.session.get(f"{self.base_url}{path}")
```

### Ключевое отличие
`self` — это `this`, но его нужно писать **явно** в каждом методе как первый аргумент. Python не прячет его. Забыл → `TypeError`. (Подробнее в NOTES.md #4)

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `this.field` (можно без `this`) | `self.field` (обязательно) | Забыл `self` → локальная переменная, не поле |
| `ClassName(args)` конструктор | `__init__(self, args)` | `__init__` = инициализатор, не конструктор |
| `get field => ...` | `@property` + `def field(self):` | Декоратор вместо синтаксиса |
| `static void fn()` | `@staticmethod` + `def fn():` | Без `self` |
| `extends Base` | `class Child(Base):` | Скобки вместо extends |
| `@override` | Просто переопределяешь | Нет `@override`, но есть `ABC` для абстрактных |
| `_private` (по конвенции) | `_private` (по конвенции) | Одинаково! Ни Dart, ни Python не запрещают доступ |
| `toString()` | `__str__()` | "Dunder" (double underscore) методы |
| `operator ==` | `__eq__()` | Все операторы — через dunder |

### Dunder-методы — минимум для тестов
| Метод | Когда вызывается | Зачем |
|-------|-----------------|-------|
| `__init__(self)` | При создании объекта | Инициализация полей |
| `__str__(self)` | `print(obj)`, `f"{obj}"` | Человеко-читаемое представление |
| `__repr__(self)` | В дебаггере, в логах | Техническое представление |
| `__eq__(self, other)` | `obj1 == obj2` | Сравнение. По умолчанию сравнивает по id (identity) |
| `__len__(self)` | `len(obj)` | Когда объект имеет "длину" |

### `@property` — геттер/сеттер без скобок
```python
class User:
    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"

# Dart: user.fullName  ← геттер
# Python: user.full_name  ← тоже без скобок, благодаря @property
```

### `@staticmethod` и `@classmethod`
```python
class MathHelper:
    @staticmethod
    def add(a: int, b: int) -> int:    # без self — как обычная функция
        return a + b

    @classmethod
    def from_string(cls, text: str):    # cls = сам класс, не экземпляр
        return cls(int(text))           # аналог factory в Dart
```
| Dart | Python | Когда |
|------|--------|-------|
| `static int add(a, b)` | `@staticmethod def add(a, b):` | Не нужен доступ к экземпляру |
| `factory User.fromJson(json)` | `@classmethod def from_json(cls, json):` | Альтернативный конструктор |

### Абстрактные классы (ABC)

```python
from abc import ABC, abstractmethod

class BasePage(ABC):
    """Нельзя создать BasePage() напрямую — только наследоваться."""

    def __init__(self, page):
        self.page = page

    @abstractmethod
    def goto(self):
        """Каждая страница ОБЯЗАНА реализовать goto()."""
        pass                    # нет реализации — наследник должен написать

    def get_title(self) -> str:
        return self.page.title()   # обычный метод — наследуется как есть

class LoginPage(BasePage):
    def goto(self):                 # ОБЯЗАН реализовать, иначе TypeError
        self.page.goto("/login")

# BasePage()     → TypeError: Can't instantiate abstract class
# LoginPage(page) → ок
```

| Dart | Python | Комментарий |
|------|--------|-------------|
| `abstract class Base { }` | `class Base(ABC):` | Наследуемся от `ABC` |
| `void method();` (без тела) | `@abstractmethod` + `pass` | Декоратор помечает метод |
| Компилятор проверяет | `TypeError` в рантайме | Python ловит при создании объекта |
| `implements` | Нет прямого — `Protocol` (typing) | Python полагается на duck typing |

**Когда использовать в тестах:** `BasePage` для UI-тестов — все страницы наследуются, обязаны реализовать `goto()`. Гарантия что не забудешь.

### Наследование и super()
```python
class BaseChecks:
    def check_status(self, response, expected: int):
        assert response.status_code == expected

class UserChecks(BaseChecks):               # наследуется от BaseChecks
    def check_user_found(self, response, user_id: int):
        self.check_status(response, 200)    # вызов метода родителя через self
        user = SingleUserResponse.model_validate(response.json())
        assert user.data.id == user_id

# super() — явный вызов родительского метода
class AdminChecks(UserChecks):
    def __init__(self):
        super().__init__()                  # вызываем __init__ родителя
        self.admin_only = True

    def check_user_found(self, response, user_id: int):
        super().check_user_found(response, user_id)  # сначала родительская проверка
        # потом дополнительная проверка
        assert response.json()["data"]["email"].endswith("@admin.com")
```

| Dart | Python | Комментарий |
|------|--------|-------------|
| `super.method()` | `super().method()` | Со скобками! `super()` возвращает proxy-объект |
| `super(args)` в конструкторе | `super().__init__(args)` | Явно вызываешь `__init__` |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `self.name = name` в `__init__` | `name = name` без self | Создашь локальную переменную, поле останется пустым |
| `@property` для вычисляемых | Публичный метод `get_name()` | В Python геттеры-методы — не идиоматично |
| Одно наследование | Множественное (если можно без него) | MRO-конфликты, сложный дебаг |
| `__str__` для пользователя, `__repr__` для дебага | Только `__str__` | В логах и дебаггере будет `<User object at 0x...>` |

### Подводные камни
1. **Забыл `self`** в определении метода → `TypeError: method() takes 0 positional arguments but 1 was given`. Самая частая ошибка (NOTES.md #4)
2. **`self.x = x`** vs **`x = x`** — без `self` это локальная переменная, она умрёт после `__init__`
3. **`is` vs `==`** — `is` сравнивает identity (один и тот же объект в памяти), `==` сравнивает значение. `None` проверяй через `is None`

### Попробуй
Открой `utils/api_client.py` и `tests/api/checks/user_checks.py`. Найди:
1. Где `__init__` инициализирует поля через `self`
2. Где `self` передаётся как первый аргумент каждого метода
3. Как Dart-разработчик, как бы ты написал `ApiClient` на Dart?

---

## 8. Декораторы

### Dart (ты это знаешь):
```dart
@override          // метаданные — подсказка компилятору
@Deprecated('Use newMethod instead')
void oldMethod() {}
```

### Python:
```python
@pytest.fixture                              # "оберни функцию в fixture"
def api_client(settings):
    return ApiClient(settings.base_url_api)

@allure.step("Проверка: пользователь найден")  # "оберни в allure-шаг"
def check_user_found(self, response, user_id):
    assert response.status_code == 200

@pytest.mark.parametrize("id", [1, 2, 3])   # "запусти 3 раза с разными данными"
def test_resource(id):
    ...
```

### Ключевое отличие
В Dart `@override` — метаданные, подсказка. В Python `@decorator` — это **реальный вызов функции**, который оборачивает твою функцию. `@pytest.fixture` буквально берёт функцию и регистрирует её как фикстуру.

### Как работает (без магии)
```python
# @decorator — это просто синтаксический сахар для:
# function = decorator(function)

# То есть:
@allure.step("Проверка")
def check(self, response): ...

# Это то же самое что:
def check(self, response): ...
check = allure.step("Проверка")(check)
```

### Декораторы которые ты встретишь в тестах
| Декоратор | Что делает | Где в проекте |
|-----------|-----------|---------------|
| `@pytest.fixture` | Регистрирует функцию как фикстуру | `conftest.py` |
| `@pytest.fixture(scope="session")` | Фикстура на всю сессию (не пересоздаётся) | `tests/conftest.py:6` |
| `@pytest.mark.parametrize` | Запускает тест N раз с разными данными | `test_resources.py` |
| `@pytest.mark.api` | Маркер — можно запустить `pytest -m api` | `test_users.py:12` |
| `@allure.feature("Users API")` | Группировка в Allure-отчёте | `test_users.py:15` |
| `@allure.story("Создание пользователя")` | Подгруппа в Allure-отчёте | `test_users.py:37` |
| `@allure.title("Текст")` | Название теста в отчёте | `test_users.py:38` |
| `@allure.severity(allure.severity_level.CRITICAL)` | Критичность в отчёте | `test_users.py:39` |
| `@allure.step("Текст")` | Шаг проверки в отчёте | `user_checks.py:10` |

### Стек декораторов — порядок имеет значение
```python
@allure.feature("Users API")      # 3. внешний слой
@allure.story("Создание")         # 2. средний слой
@allure.title("Создать юзера")    # 1. внутренний слой
def test_create_user(self):
    ...
```
Декораторы применяются **снизу вверх** — ближайший к `def` первый.

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| Стек: feature → story → title → severity | Хаотичный порядок | Allure-отчёт будет неструктурированным |
| `@pytest.mark.api` на уровне модуля: `pytestmark = pytest.mark.api` | На каждом тесте отдельно | Дублирование, легко забыть |
| Читай декоратор как "этот тест/фикстура делает..." | Просто копируй не разбираясь | Дебажить декораторы сложно если не понимаешь механизм |

### Подводные камни
1. **`@pytest.mark.parametrize`** — пишется именно так, не `parameterize`! (NOTES.md #3)
2. **Забыл скобки** — `@pytest.fixture` работает, `@pytest.fixture()` тоже, но `@allure.step` без скобок и аргумента — нет
3. **Порядок** — `@staticmethod` должен быть последним (ближе всего к `def`), иначе `self` сломается

### Попробуй
Открой `tests/api/test_users.py`. Посчитай все декораторы в файле:
1. Сколько разных типов декораторов используется?
2. Что делает `pytestmark = pytest.mark.api` на строке 12?
3. Чем `@allure.feature` отличается от `@allure.story`?

---

## 9. Контекстные менеджеры

### Dart (ты это знаешь):
```dart
final file = File('data.txt');
try {
  final content = await file.readAsString();
  // работаем с файлом
} finally {
  // Dart: GC закроет сам, но для сокетов нужен close()
  await socket.close();
}
```

### Python:
```python
# with — автоматически закрывает ресурс при выходе из блока
with open("data.txt") as file:
    content = file.read()
# файл гарантированно закрыт, даже если было исключение

# requests.Session как context manager
with requests.Session() as session:
    response = session.get("https://api.com/users")
# сессия закрыта, соединения освобождены
```

### Ключевое отличие
`with` — это `try/finally` в одну строку. Python гарантирует вызов "закрытия" (метод `__exit__`) даже при исключении. В Dart GC делает часть работы, но для ресурсов (файлы, соединения) нужен `finally`.

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `try { } finally { close() }` | `with resource as x:` | `with` — идиоматичнее и безопаснее |
| GC + `close()` | `with` / `__enter__` + `__exit__` | Python явно управляет ресурсами |
| Нет аналога | Можно писать свои через `@contextmanager` | Для будущего — пока не нужно |

### Где встретишь в тестах
```python
# Playwright — ожидание навигации
with page.expect_navigation():
    page.click("a.link")

# Файлы (allure-вложения, конфиги)
with open("config.json") as f:
    config = json.load(f)
```

### Подводные камни
1. **Забыл `with`** → файл не закроется до GC. При 1000 тестов → "Too many open files"
2. **`as` опционален** — `with open("f"):` работает, если не нужна переменная

---

## 10. Обработка ошибок

### Dart (ты это знаешь):
```dart
try {
  final result = json.decode(response.body);
} on FormatException catch (e) {
  print('Не JSON: $e');
} catch (e) {
  print('Другая ошибка: $e');
} finally {
  cleanup();
}
```

### Python:
```python
try:
    result = response.json()
except ValueError:                 # конкретное исключение
    result = response.text
except Exception as e:             # всё остальное
    print(f"Ошибка: {e}")
else:                              # НЕТ в Dart — выполнится если НЕ было ошибки
    process(result)
finally:
    cleanup()
```

### Ключевое отличие
В Python есть блок `else` — код, который выполняется **только если исключения не было**. В Dart этого нет. Это полезно чтобы не ловить исключения из кода обработки.

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `on TypeError catch (e)` | `except TypeError as e:` | Ловим конкретный тип |
| `catch (e)` | `except Exception as e:` | Ловим всё |
| `rethrow;` | `raise` (без аргументов) | Пробросить дальше |
| `throw Exception('msg')` | `raise ValueError('msg')` | Кинуть исключение |
| Нет аналога | `else:` | Код при успехе (без ошибки) |
| `finally { }` | `finally:` | Идентично |

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `except ValueError:` — конкретное | `except:` — голый except | Поймаешь даже `KeyboardInterrupt` (Ctrl+C) — не сможешь остановить |
| `except Exception as e:` если правда нужно всё | `except Exception:` без `as e` | Не узнаешь что за ошибка |
| Логируй ошибку перед `pass` | `except: pass` | Тихо проглотишь ошибку, будешь дебажить часами |

### Подводные камни
1. **`except:` без типа** — ловит абсолютно всё, включая `SystemExit` и `KeyboardInterrupt`. Всегда указывай тип
2. **`else` путают с `finally`** — `else` = "если ок", `finally` = "в любом случае"
3. **Python исключения — это классы** с наследованием: `ValueError` → `Exception` → `BaseException`

### Попробуй
Открой `utils/api_client.py:27-29`. Найди `try/except ValueError`:
1. Почему именно `ValueError`, а не `Exception`?
2. Что произойдёт если `response.json()` вернёт не JSON?

---

## 11. Type hints

### Dart (ты это знаешь):
```dart
String greet(String name) => 'Hello, $name';  // типы обязательны (по умолчанию)
int? maybeNull;                                // nullable
List<String> names;                            // generic
```

### Python:
```python
def greet(name: str) -> str:          # type hints — подсказки, не требования
    return f"Hello, {name}"

maybe_null: str | None = None         # Python 3.10+ — Union через |
maybe_null: Optional[str] = None      # Python 3.9  — через Optional

names: list[str] = []                 # generic (Python 3.9+)
```

### Ключевое отличие
В Dart типы **обязательны** и проверяются компилятором. В Python type hints — **подсказки для IDE и линтера**, Python их игнорирует в рантайме. Но Pydantic **проверяет** типы в рантайме — это мост к Dart-подходу.

### Сравнение
| Dart | Python 3.9+ | Комментарий |
|------|-------------|-------------|
| `String` | `str` | Маленькая буква |
| `int` | `int` | Одинаково |
| `double` | `float` | Другое имя |
| `bool` | `bool` | Одинаково |
| `List<String>` | `list[str]` | Маленькая `l`, квадратные скобки |
| `Map<String, int>` | `dict[str, int]` | `dict` вместо `Map` |
| `int?` | `int \| None` или `Optional[int]` | `None` вместо `null` |
| `dynamic` | `Any` (из `typing`) | "Любой тип" |
| `void` | `-> None` | Возвращаемый тип |
| `Future<String>` | Нет прямого аналога | `async def` → Coroutine, но в тестах не нужно |

### Pydantic — type hints с зубами
```python
from pydantic import BaseModel

class UserData(BaseModel):
    id: int                    # обязательное, проверяется в рантайме!
    email: str
    name: str = ""             # дефолт

user = UserData.model_validate({"id": 1, "email": "a@b.com"})
# name будет "", id и email проверятся

user = UserData.model_validate({"id": "not_a_number", "email": "a@b.com"})
# ValidationError! Pydantic не пропустит строку вместо int
```
Dart-аналог: `fromJson` с ручной валидацией, или `freezed`. Pydantic делает это автоматически.

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `list[str]` (Python 3.9+) | `from typing import List; List[str]` | Старый стиль, лишний импорт |
| `x: int \| None = None` (3.10+) | `x: Optional[int] = None` | `Optional` менее читаемый |
| Type hints на параметрах и возвращаемых | Только на параметрах | IDE не поможет вызывающему коду |
| Pydantic для внешних данных (API) | Ручная валидация `if "key" in dict` | Pydantic даёт бесплатную валидацию + документацию |

### Подводные камни
1. **Type hints не проверяются Python!** `def fn(x: int): ...` → `fn("hello")` — Python не ругнётся. Только IDE/mypy/ruff покажут ошибку
2. **`Optional[str]` ≠ "необязательный параметр"** — это `str | None`. Параметр всё ещё может быть обязательным
3. **Python 3.9 vs 3.10** — `list[str]` работает с 3.9, `int | str` — с 3.10. В нашем проекте 3.9+, поэтому `Optional` для union-типов

### Попробуй
Открой `tests/api/models.py`. Посмотри как Pydantic-модели используют type hints:
1. Чем `id: int` отличается от `name: str = ""`?
2. Что будет если API вернёт `{"id": "abc"}` для `UserData`?
3. Как бы ты написал `UserData` в Dart (с `fromJson`)?

---

## 12. Генераторы и yield

### Dart (ты это знаешь):
```dart
// Stream — ленивая последовательность
Stream<int> countTo(int n) async* {
  for (var i = 0; i < n; i++) {
    yield i;
  }
}
```

### Python:
```python
# генератор — функция с yield вместо return
def count_to(n: int):
    for i in range(n):
        yield i            # "отдаёт" значение и засыпает

for num in count_to(5):
    print(num)             # 0, 1, 2, 3, 4
```

### Зачем в тестах?
В pytest `yield` используется для **setup/teardown** в фикстурах:

```python
@pytest.fixture
def browser():
    driver = webdriver.Chrome()       # setup — до yield
    yield driver                       # отдаём фикстуру тесту
    driver.quit()                      # teardown — после yield, ВСЕГДА выполнится

# аналог в Dart:
# setUp(() => driver = ChromeDriver());
# tearDown(() => driver.quit());
```

### Ключевое отличие
`yield` в фикстуре = `setUp` + `tearDown` в одной функции. Код до `yield` — подготовка, после — очистка.

### Итераторы — протокол под капотом

Генератор — это **частный случай итератора**. Итератор — любой объект с методами `__iter__` и `__next__`.

```python
# Как работает for под капотом:
for item in [1, 2, 3]:
    print(item)

# Python делает:
iterator = iter([1, 2, 3])      # вызывает list.__iter__()
print(next(iterator))            # 1  — вызывает iterator.__next__()
print(next(iterator))            # 2
print(next(iterator))            # 3
print(next(iterator))            # StopIteration! — цикл завершается
```

### Свой итератор (для понимания, не для тестов)

```python
class Countdown:
    """Обратный отсчёт: Countdown(3) → 3, 2, 1"""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self                 # итератор = сам объект

    def __next__(self):
        if self.current <= 0:
            raise StopIteration     # сигнал "больше нечего отдавать"
        value = self.current
        self.current -= 1
        return value

for num in Countdown(3):
    print(num)                      # 3, 2, 1
```

| Dart | Python | Комментарий |
|------|--------|-------------|
| `Iterable<T>` | `__iter__()` | Возвращает итератор |
| `Iterator<T>.moveNext()` | `__next__()` | Следующий элемент |
| `Iterator.current` | Возвращается из `__next__` | Нет отдельного `.current` |
| `StopIteration` нет | `raise StopIteration` | Сигнал конца |

**Когда встретишь в тестах:** почти никогда напрямую. Но `for item in items:`, `list()`, `dict()` — всё это использует итераторы под капотом. Знание протокола помогает понять ошибки типа `TypeError: 'int' object is not iterable`.

### Подводные камни
1. **`return` vs `yield`** — `return` завершает функцию, `yield` приостанавливает. Функция с `yield` — уже не обычная функция, а генератор
2. **Один `yield` в фикстуре** — можно иметь только один yield. Два → ошибка
3. **Итератор одноразовый** — прошёлся один раз → `StopIteration`. Для повторного обхода нужен новый итератор

---

## 13. Модули и пакеты

### Dart (ты это знаешь):
```dart
import 'package:http/http.dart' as http;       // пакет
import '../models/user.dart';                   // относительный
import 'package:my_app/utils/helpers.dart';     // абсолютный
```

### Python:
```python
import json                                     # стандартная библиотека
import requests                                 # pip-пакет (внешний)
from pydantic import BaseModel                  # конкретный класс из пакета
from tests.api.checks.user_checks import UserChecks  # из проекта (абсолютный)
from ..models import UserData                   # относительный (редко используем)
```

### Ключевое отличие
В Dart `import` — по пути к файлу. В Python `import` — по **пути к модулю** (точки вместо слэшей). Каждая папка с `__init__.py` — это пакет. Без `__init__.py` Python не видит папку (NOTES.md #2).

### Сравнение
| Dart | Python | Комментарий |
|------|--------|-------------|
| `import 'pkg:http/http.dart'` | `import requests` | Без пути, по имени пакета |
| `import '...' as alias` | `import requests as req` | Алиасы одинаковы |
| `import '...' show Class` | `from module import Class` | Импорт конкретного имени |
| `import '...' hide Class` | Нет аналога | Python: просто не импортируй |
| `part` / `part of` | Нет аналога | В Python каждый файл — самостоятельный модуль |
| Нет аналога | `__init__.py` | "Табличка ОТКРЫТО" — делает папку пакетом |

### Цепочка импортов в нашем проекте
```
test_users.py
  └── from tests.api.test_data import EXISTING_USER_ID
  └── conftest.py (pytest находит автоматически)
        └── from tests.api.checks.user_checks import UserChecks
        └── from utils.api_client import ApiClient
              └── import requests
              └── import allure
        └── tests/conftest.py
              └── from config.config import settings
```

### Порядок импортов (ruff следит за этим)
```python
# 1. Стандартная библиотека
import json
import logging

# 2. Сторонние пакеты (pip)
import allure
import requests

# 3. Свой код проекта
from tests.api.models import UserData
from utils.api_client import ApiClient
```

### Лучшие практики
| Делай так | Не делай так | Что произойдёт |
|-----------|-------------|----------------|
| `from module import Class` | `from module import *` | `*` засоряет namespace, непонятно откуда что |
| Абсолютные импорты | Относительные `from ..module` | Абсолютные — понятнее, не ломаются при перемещении |
| `__init__.py` в каждой папке-пакете | Забыть создать | `ImportError` — Python не видит папку |
| Группировка: stdlib → pip → проект | Всё вперемешку | ruff выдаст ошибку `I001` |

### Подводные камни
1. **Циклические импорты** — A импортирует B, B импортирует A → `ImportError`. Решение: вынести общее в третий модуль
2. **`__init__.py` на каждом уровне** — `tests/api/checks/` — нужен `__init__.py` и в `tests/`, и в `api/`, и в `checks/` (NOTES.md #2)
3. **Имя файла = имя модуля** — не называй файл `test.py` или `string.py` — перекроешь стандартную библиотеку

### Попробуй
Открой `tests/api/conftest.py` и проследи всю цепочку:
1. Откуда берётся `ApiClient`?
2. Откуда берётся `settings` (аргумент фикстуры `api_client`)?
3. Сколько `__init__.py` файлов нужно чтобы импорт `from tests.api.checks.user_checks import UserChecks` работал?

---

## 14. Питонические идиомы

Цель — писать Python, а не "Dart на Python".

### Unpacking — множественное присваивание
```python
# Dart:
# final first = pair[0]; final second = pair[1];

# Python:
first, second = (10, 20)                     # tuple unpacking
name, age, *rest = ["Alice", 30, "dev", "NY"]  # rest = ["dev", "NY"]

# swap без temp
a, b = b, a                                  # Dart: final tmp = a; a = b; b = tmp;
```

### Таблица "Dart-style vs Pythonic"
| Dart-style (работает, но не пиши так) | Pythonic (пиши так) | Почему |
|--------------------------------------|---------------------|--------|
| `for i in range(len(items)):` + `items[i]` | `for item in items:` | Прямой доступ, без индекса |
| `for i in range(len(items)):` + `print(i, items[i])` | `for i, item in enumerate(items):` | `enumerate` даёт индекс + элемент |
| `i = 0; while i < n: ... i += 1` | `for i in range(n):` | `range` — идиоматичнее |
| `result = []; for x in items: result.append(f(x))` | `result = [f(x) for x in items]` | Comprehension — быстрее и чище |
| `if len(items) > 0:` | `if items:` | Truthiness: пустой список = False |
| `if x == True:` | `if x:` | Truthiness опять |
| `if x == None:` | `if x is None:` | `is` для None — identity check |
| `try: d["key"] except: d["key"] = value` | `d.setdefault("key", value)` | Один вызов |
| Вложенные `if` | Ранний `return` | Меньше вложенность — читаемее |

### Полезные встроенные функции
| Функция | Dart аналог | Что делает | Пример |
|---------|------------|-----------|--------|
| `enumerate(list)` | Нет прямого | Индекс + элемент | `for i, x in enumerate(items):` |
| `zip(a, b)` | Нет прямого | Параллельный обход | `for x, y in zip(names, ages):` |
| `any(cond for x in list)` | `list.any((x) => cond)` | Хотя бы один True | `any(u.active for u in users)` |
| `all(cond for x in list)` | `list.every((x) => cond)` | Все True | `all(r.status == 200 for r in responses)` |
| `sorted(list, key=fn)` | `list..sort((a,b) => ...)` | Сортировка | `sorted(users, key=lambda u: u.name)` |
| `len(x)` | `x.length` | Длина | Функция, не свойство! |
| `type(x)` | `x.runtimeType` | Тип объекта | Для дебага |
| `isinstance(x, str)` | `x is String` | Проверка типа | Идиоматичнее чем `type(x) == str` |

### Тернарный оператор
```python
# Dart:
# final label = isAdmin ? "Admin" : "User";

# Python:
label = "Admin" if is_admin else "User"
# Читается как предложение: "Admin если is_admin иначе User"
```

### EAFP vs LBYL
```python
# LBYL (Look Before You Leap) — Dart-стиль
if "key" in dict:
    value = dict["key"]

# EAFP (Easier to Ask Forgiveness) — Python-стиль
try:
    value = dict["key"]
except KeyError:
    value = default

# Но лучше всего:
value = dict.get("key", default)
```

### Подводные камни
1. **`or` для дефолтов** — `name = user_name or "Anonymous"`. Но `0 or "Anonymous"` → `"Anonymous"`! Ноль — falsy
2. **`is` vs `==`** — `is` для `None`, `True`, `False`. Для всего остального — `==`
3. **`range(5)` начинается с 0** и не включает 5 → `[0, 1, 2, 3, 4]`. Как Dart `List.generate(5, (i) => i)`

### Попробуй
Перепиши этот "Dart-style" Python в идиоматичный Python:
```python
# До (Dart-style):
result = []
for i in range(len(users)):
    if users[i].status == 200:
        result.append(users[i].name)
if len(result) > 0:
    print("Found: " + str(len(result)))

# После (Pythonic):
# ???
```

---

---
---

# НАВИГАЦИЯ

| Файл | Что внутри |
|------|-----------|
| [00 — Шпаргалка для собеса](00_interview_cheatsheet.md) | Определения + подвох-вопросы |
| **01 — Python язык** | **Ты здесь** |
| [02 — API-тестирование](02_api_testing.md) | requests + pytest + Pydantic |
| [03 — UI-тестирование](03_ui_testing.md) | Playwright Python |
| [NOTES.md](../NOTES.md) | Вопросы и ответы по ходу работы |
