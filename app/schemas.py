import re
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class Major(str, Enum):
    informatics = "Информатика"
    economics = "Экономика"
    law = "Право"
    medicine = "Медицина"
    engineering = "Инженерия"
    languages = "Языки"


class Student(BaseModel):
    student_id: int = Field(
        description="Уникальный идентификатор студента"
    )

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя студента"
    )

    last_name: str = Field(
        min_length=1,
        max_length=50,
        description="Фамилия студента"
    )

    date_of_birth: date = Field(
        description="Дата рождения студента в формате YYYY-MM-DD"
    )

    email: EmailStr = Field(
        description="Электронная почта студента"
    )

    phone_number: str = Field(
        description="Номер телефона"
    )

    address: str = Field(
        min_length=5,
        max_length=200,
        description="Адрес студента"
    )

    enrollment_year: int = Field(
        ge=2000,
        le=2030,
        description="Год поступления"
    )

    major: Major = Field(
        description="Специальность студента"
    )

    course: int = Field(
        ge=1,
        le=5,
        description="Курс студента"
    )

    special_notes: Optional[str] = Field(
        default="Без особых примет",
        max_length=500,
        description="Дополнительные заметки"
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

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date) -> date:
        if value >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")

        return value


class StudentUpdate(BaseModel):
    course: int = Field(
        ge=1,
        le=5,
        description="Новый курс студента"
    )

    major: Major = Field(
        description="Новая специальность студента"
    )
