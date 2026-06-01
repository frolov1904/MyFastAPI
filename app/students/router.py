from fastapi import APIRouter, HTTPException, status

from app.students.dao import MajorDAO, StudentDAO
from app.students.schemas import (
    MajorCreate,
    MajorRead,
    StudentCreate,
    StudentRead,
    StudentUpdate,
)


router = APIRouter(
    tags=["Студенты и специальности"],
)


@router.get("/majors", response_model=list[MajorRead])
async def get_majors():
    return await MajorDAO.find_all()


@router.post("/majors", response_model=MajorRead, status_code=status.HTTP_201_CREATED)
async def add_major(major: MajorCreate):
    existing_major = await MajorDAO.find_one_or_none(major_name=major.major_name)

    if existing_major:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такая специальность уже существует",
        )

    return await MajorDAO.add(**major.model_dump())


@router.get("/students", response_model=list[StudentRead])
async def get_students():
    return await StudentDAO.find_all()


@router.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentCreate):
    major = await MajorDAO.find_one_or_none_by_id(student.major_id)

    if not major:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Специальность с таким major_id не найдена",
        )

    existing_email = await StudentDAO.find_one_or_none(email=student.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Студент с таким email уже существует",
        )

    existing_phone = await StudentDAO.find_one_or_none(phone_number=student.phone_number)

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Студент с таким номером телефона уже существует",
        )

    return await StudentDAO.add(**student.model_dump())


@router.put("/students/{student_id}", response_model=StudentRead)
async def update_student(student_id: int, student_data: StudentUpdate):
    values = student_data.model_dump(exclude_unset=True)

    if not values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для обновления",
        )

    if "major_id" in values:
        major = await MajorDAO.find_one_or_none_by_id(values["major_id"])

        if not major:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Специальность с таким major_id не найдена",
            )

    updated_student = await StudentDAO.update(
        {"id": student_id},
        **values,
    )

    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент с таким id не найден",
        )

    return updated_student


@router.delete("/students/{student_id}", response_model=StudentRead)
async def delete_student(student_id: int):
    deleted_student = await StudentDAO.delete(id=student_id)

    if not deleted_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент с таким id не найден",
        )

    return deleted_student