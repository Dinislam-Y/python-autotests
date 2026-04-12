from faker import Faker

# фейкер с русской локалью — пригодится для генерации тестовых данных
fake = Faker("ru_RU")


def random_user():
    """Случайный юзер для POST /api/users — когда лень придумывать имена."""
    return {
        "name": fake.first_name(),
        "job": fake.job(),
    }
