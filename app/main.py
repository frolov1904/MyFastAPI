from fastapi import FastAPI

from app.students.router import router as students_router


app = FastAPI(
    title="MyFastAPI",
    description="Учебный API для работы со студентами и специальностями",
    version="0.4.0",
)

app.include_router(students_router)


@app.get("/")
def home_page():
    return {"message": "API работает"}