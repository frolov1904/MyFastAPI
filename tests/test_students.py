import pytest

from app.users.dao import UsersDAO


async def register_user(
    client,
    email: str = "alex@example.com",
    phone_number: str = "+79991234567",
):
    return await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456",
            "phone_number": phone_number,
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )


async def login_user(
    client,
    email: str = "alex@example.com",
    password: str = "123456",
):
    return await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


async def make_user_admin(email: str = "alex@example.com"):
    return await UsersDAO.update(
        {"email": email},
        is_admin=True,
    )


async def create_admin_and_login(client):
    await register_user(
        client,
        email="admin@example.com",
        phone_number="+79990000000",
    )

    await make_user_admin(email="admin@example.com")

    return await login_user(
        client,
        email="admin@example.com",
    )


async def create_major_as_admin(client):
    await create_admin_and_login(client)

    return await client.post(
        "/majors",
        json={
            "major_name": "Информатика",
            "major_description": "Направление, связанное с программированием",
        },
    )


@pytest.mark.asyncio
async def test_get_majors_available_without_auth(client):
    response = await client.get("/majors")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_students_available_without_auth(client):
    response = await client.get("/students")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_major_without_auth_forbidden(client):
    response = await client.post(
        "/majors",
        json={
            "major_name": "Информатика",
            "major_description": "Направление, связанное с программированием",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Токен отсутствует"


@pytest.mark.asyncio
async def test_create_major_by_regular_user_forbidden(client):
    await register_user(client)
    await login_user(client)

    response = await client.post(
        "/majors",
        json={
            "major_name": "Информатика",
            "major_description": "Направление, связанное с программированием",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Недостаточно прав"


@pytest.mark.asyncio
async def test_create_major_by_admin(client):
    response = await create_major_as_admin(client)

    assert response.status_code == 201

    data = response.json()

    assert data["major_name"] == "Информатика"
    assert data["major_description"] == "Направление, связанное с программированием"
    assert data["count_students"] == 0


@pytest.mark.asyncio
async def test_create_student_without_auth_forbidden(client):
    major_response = await create_major_as_admin(client)
    major_id = major_response.json()["id"]

    await client.post("/auth/logout")

    response = await client.post(
        "/students",
        json={
            "phone_number": "+79991234567",
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "2002-04-10",
            "email": "ivan@example.com",
            "address": "г. Москва, ул. Тестовая, д. 1",
            "enrollment_year": 2022,
            "course": 2,
            "special_notes": "Тестовый студент",
            "major_id": major_id,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Токен отсутствует"


@pytest.mark.asyncio
async def test_create_student_by_authorized_user(client):
    major_response = await create_major_as_admin(client)
    major_id = major_response.json()["id"]

    await client.post("/auth/logout")

    await register_user(
        client,
        email="user@example.com",
        phone_number="+79991111111",
    )
    await login_user(
        client,
        email="user@example.com",
    )

    response = await client.post(
        "/students",
        json={
            "phone_number": "+79991234567",
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "2002-04-10",
            "email": "ivan@example.com",
            "address": "г. Москва, ул. Тестовая, д. 1",
            "enrollment_year": 2022,
            "course": 2,
            "special_notes": "Тестовый студент",
            "major_id": major_id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["first_name"] == "Иван"
    assert data["last_name"] == "Иванов"
    assert data["email"] == "ivan@example.com"
    assert data["major_id"] == major_id


@pytest.mark.asyncio
async def test_update_student_by_authorized_user(client):
    major_response = await create_major_as_admin(client)
    major_id = major_response.json()["id"]

    await client.post("/auth/logout")

    await register_user(
        client,
        email="user@example.com",
        phone_number="+79991111111",
    )
    await login_user(
        client,
        email="user@example.com",
    )

    student_response = await client.post(
        "/students",
        json={
            "phone_number": "+79991234567",
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "2002-04-10",
            "email": "ivan@example.com",
            "address": "г. Москва, ул. Тестовая, д. 1",
            "enrollment_year": 2022,
            "course": 2,
            "special_notes": "Тестовый студент",
            "major_id": major_id,
        },
    )

    student_id = student_response.json()["id"]

    update_response = await client.put(
        f"/students/{student_id}",
        json={
            "course": 3,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == student_id
    assert data["course"] == 3


@pytest.mark.asyncio
async def test_delete_student_by_regular_user_forbidden(client):
    major_response = await create_major_as_admin(client)
    major_id = major_response.json()["id"]

    student_response = await client.post(
        "/students",
        json={
            "phone_number": "+79991234567",
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "2002-04-10",
            "email": "ivan@example.com",
            "address": "г. Москва, ул. Тестовая, д. 1",
            "enrollment_year": 2022,
            "course": 2,
            "special_notes": "Тестовый студент",
            "major_id": major_id,
        },
    )

    student_id = student_response.json()["id"]

    await client.post("/auth/logout")

    await register_user(
        client,
        email="user@example.com",
        phone_number="+79991111111",
    )
    await login_user(
        client,
        email="user@example.com",
    )

    delete_response = await client.delete(f"/students/{student_id}")

    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "Недостаточно прав"


@pytest.mark.asyncio
async def test_delete_student_by_admin(client):
    major_response = await create_major_as_admin(client)
    major_id = major_response.json()["id"]

    student_response = await client.post(
        "/students",
        json={
            "phone_number": "+79991234567",
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "2002-04-10",
            "email": "ivan@example.com",
            "address": "г. Москва, ул. Тестовая, д. 1",
            "enrollment_year": 2022,
            "course": 2,
            "special_notes": "Тестовый студент",
            "major_id": major_id,
        },
    )

    student_id = student_response.json()["id"]

    delete_response = await client.delete(f"/students/{student_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == student_id

    students_response = await client.get("/students")

    assert students_response.status_code == 200
    assert students_response.json() == []