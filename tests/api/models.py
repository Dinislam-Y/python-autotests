from pydantic import BaseModel


# модели ответов reqres.in — валидирую структуру, а не просто status_code
# если API поменяет формат, тесты упадут на парсинге, а не молча пропустят


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Support(BaseModel):
    url: str
    text: str


class SingleUserResponse(BaseModel):
    data: UserData
    support: Support


class UserListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]
    support: Support


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UpdateUserResponse(BaseModel):
    # PATCH может вернуть только изменённые поля, name не всегда приходит
    name: str = ""
    job: str
    updatedAt: str


class RegisterResponse(BaseModel):
    id: int
    token: str


class LoginResponse(BaseModel):
    token: str


class ErrorResponse(BaseModel):
    error: str
