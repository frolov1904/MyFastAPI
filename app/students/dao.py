from app.dao.base import BaseDAO
from app.students.models import Major, Student


class StudentDAO(BaseDAO):
    model = Student


class MajorDAO(BaseDAO):
    model = Major