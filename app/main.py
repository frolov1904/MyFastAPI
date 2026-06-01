from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.pages.router import router as pages_router
from app.students.router import router as students_router
from app.users.router import router as users_router


app = FastAPI(
    title="MyFastAPI",
    description="Учебный API для работы со студентами и специальностями",
    version="0.7.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(students_router)
app.include_router(users_router)
app.include_router(pages_router)


@app.get("/")
def home_page():
    return {"message": "API работает"}