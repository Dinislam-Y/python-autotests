import pytest

from config.config import settings as app_settings


@pytest.fixture(scope="session")
def settings():
    """Настройки проекта — один раз на всю сессию, нет смысла пересоздавать."""
    return app_settings
