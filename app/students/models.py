from datetime import date

from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_nullable, str_uniq


class Student(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    course: Mapped[int]
    special_notes: Mapped[str_nullable]

    major_id: Mapped[int] = mapped_column(
        ForeignKey("majors.id"),
        nullable=False,
    )

    major: Mapped["Major"] = relationship(
        "Major",
        back_populates="students",
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r})"
        )

    def __repr__(self) -> str:
        return str(self)


class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_nullable]
    count_students: Mapped[int] = mapped_column(server_default=text("0"))

    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="major",
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"major_name={self.major_name!r})"
        )

    def __repr__(self) -> str:
        return str(self)