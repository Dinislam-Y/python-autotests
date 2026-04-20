from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# модели ответов reqres.in — валидирую структуру, а не просто status_code
# если API поменяет формат или подмешает лишние поля, тесты упадут на парсинге


class ContractModel(BaseModel):
    """Базовая схема API — лишние поля считаю нарушением контракта."""

    model_config = ConfigDict(extra="forbid")


class MetaCta(ContractModel):
    label: str
    url: str


class ResponseMeta(ContractModel):
    powered_by: str
    docs_url: str
    upgrade_url: str
    example_url: str
    variant: str
    message: str
    cta: MetaCta
    context: str


class SuccessResponse(ContractModel):
    # reqres добавляет служебный _meta почти во все успешные JSON-ответы
    meta: ResponseMeta = Field(alias="_meta")


class UserData(ContractModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Support(ContractModel):
    url: str
    text: str


class SingleUserResponse(SuccessResponse):
    data: UserData
    support: Support


class UserListResponse(SuccessResponse):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]
    support: Support


class CreateUserResponse(SuccessResponse):
    name: str
    job: str
    id: str
    createdAt: datetime


class UpdateUserResponse(SuccessResponse):
    # PATCH может вернуть только изменённые поля, name не всегда приходит
    name: Optional[str] = None
    job: str
    updatedAt: datetime


class RegisterResponse(SuccessResponse):
    id: int
    token: str


class LoginResponse(SuccessResponse):
    token: str


class ErrorResponse(ContractModel):
    error: str


class ResourceData(ContractModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class SingleResourceResponse(SuccessResponse):
    data: ResourceData
    support: Support


class ResourceListResponse(SuccessResponse):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[ResourceData]
    support: Support
