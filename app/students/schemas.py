import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class MajorCreate(BaseModel):
    major_name: str = Field(
        min_length=1,
        max_length=100,
        description="Название специальности",
    )

    major_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Описание специальности",
    )


class MajorRead(BaseModel):
    id: int
    major_name: str
    major_description: Optional[str]
    count_students: int

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    phone_number: str = Field(description="Номер телефона")
    first_name: str = Field(min_length=1, max_length=50, description="Имя студента")
    last_name: str = Field(min_length=1, max_length=50, description="Фамилия студента")
    date_of_birth: date = Field(description="Дата рождения")
    email: EmailStr = Field(description="Электронная почта")
    address: str = Field(min_length=5, max_length=200, description="Адрес")
    enrollment_year: int = Field(ge=2000, le=2030, description="Год поступления")
    course: int = Field(ge=1, le=5, description="Курс")
    special_notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Дополнительные заметки",
    )
    major_id: int = Field(description="ID специальности из таблицы majors")

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
    course: Optional[int] = Field(default=None, ge=1, le=5)
    major_id: Optional[int] = Field(default=None)


class StudentRead(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    address: str
    enrollment_year: int
    course: int
    special_notes: Optional[str]
    major_id: int

    model_config = ConfigDict(from_attributes=True)