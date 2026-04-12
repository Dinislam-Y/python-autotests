from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта — тянутся из .env или берутся дефолтные."""

    # тестируемые сервисы
    base_url_ui: str = "https://cms-dev.tochka-school.ru"
    base_url_api: str = "https://reqres.in"

    # reqres.in — бесплатный ключ, получить на app.reqres.in/signup
    api_key: str = ""

    # playwright
    browser: str = "chromium"
    headless: bool = True
    timeout: int = 30000  # 30 сек — хватает даже для медленного dev-стенда

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# один экземпляр на весь проект, импортируем его
settings = Settings()
