import os
from typing import Optional

from fastapi import FastAPI, HTTPException

from app.schemas import Student, StudentUpdate
from utils import dict_list_to_json, json_to_dict_list

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'students.json')

app = FastAPI()


@app.get("/")
# корневая директория
def home_page():
    return {"message": "Привет!"}


@app.get("/students")
# Optional:Благодаря этому мы не только указали, что FastApi должен ждать целое число (int), но и разрешили вообще не передавать этот параметр (параметр запроса).
def get_all_students(course: Optional[int] = None):
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list


@app.get("/students/{course}")
def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    for student in students:
        if student["course"] == course:
            filtered_students.append(student)

    if major:
        filtered_students = [
            student for student in filtered_students if student['major'].lower() == major.lower()]

    if enrollment_year:
        filtered_students = [
            student for student in filtered_students if student['enrollment_year'] == enrollment_year]

    return filtered_students


@app.post("/students")
def add_student(student: Student):
    students = json_to_dict_list(path_to_json)

    for existing_student in students:
        if existing_student["student_id"] == student.student_id:
            raise HTTPException(
                status_code=400,
                detail="Студент с таким student_id уже существует",
            )

    students.append(student.model_dump(mode="json"))

    is_saved = dict_list_to_json(students, path_to_json)

    if not is_saved:
        raise HTTPException(
            status_code=500,
            detail="Ошибка при сохранении студента",
        )

    return {
        "message": "Студент успешно добавлен",
        "student": student,
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, new_data: StudentUpdate):
    students = json_to_dict_list(path_to_json)

    for student in students:
        if student["student_id"] == student_id:
            update_data = new_data.model_dump(mode="json")

            student.update(update_data)

            is_saved = dict_list_to_json(students, path_to_json)

            if not is_saved:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при сохранении изменений",
                )

            return {
                "message": "Информация о студенте успешно обновлена",
                "student": student,
            }

    raise HTTPException(
        status_code=404,
        detail="Студент с таким student_id не найден",
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = json_to_dict_list(path_to_json)

    for index, student in enumerate(students):
        if student["student_id"] == student_id:
            deleted_student = students.pop(index)

            is_saved = dict_list_to_json(students, path_to_json)

            if not is_saved:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при удалении студента",
                )

            return {
                "message": "Студент успешно удален",
                "student": deleted_student,
            }

    raise HTTPException(
        status_code=404,
        detail="Студент с таким student_id не найден",
    )
