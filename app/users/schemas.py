import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя")

    password: str = Field(
        min_length=6,
        max_length=50,
        description="Пароль пользователя",
    )

    phone_number: str = Field(description="Номер телефона пользователя")

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )

    last_name: str = Field(
        min_length=1,
        max_length=50,
        description="Фамилия пользователя",
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        pattern = r"^\+[\d\s().-]{7,25}$"

        if not re.match(pattern, value):
            raise ValueError(
                "Номер телефона должен начинаться с '+' и содержать только цифры, пробелы, скобки, точки или дефисы"
            )

        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя")
    password: str = Field(description="Пароль пользователя")


class UserRead(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    is_user: bool
    is_student: bool
    is_teacher: bool
    is_admin: bool
    is_super_admin: bool

    model_config = ConfigDict(from_attributes=True)