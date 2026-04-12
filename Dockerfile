# образ от Microsoft — уже есть Python + Playwright + браузеры
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

# сначала копирую только зависимости — кешируется при пересборке
COPY pyproject.toml .
RUN pip install -e "."

# теперь весь проект
COPY . .

CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]
