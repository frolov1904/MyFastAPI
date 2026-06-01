import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "alex@example.com",
            "password": "123456",
            "phone_number": "+79991234567",
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "alex@example.com"
    assert data["phone_number"] == "+79991234567"
    assert data["first_name"] == "Алексей"
    assert data["last_name"] == "Фролов"
    assert "hashed_password" not in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_user_with_existing_email(client):
    user_data = {
        "email": "alex@example.com",
        "password": "123456",
        "phone_number": "+79991234567",
        "first_name": "Алексей",
        "last_name": "Фролов",
    }

    first_response = await client.post("/auth/register", json=user_data)

    second_response = await client.post(
        "/auth/register",
        json={
            **user_data,
            "phone_number": "+79990000000",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Пользователь с таким email уже существует"


@pytest.mark.asyncio
async def test_login_user(client):
    await client.post(
        "/auth/register",
        json={
            "email": "alex@example.com",
            "password": "123456",
            "phone_number": "+79991234567",
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "alex@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Пользователь успешно авторизован"
    assert "access_token" in data
    assert "users_access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_user_with_wrong_password(client):
    await client.post(
        "/auth/register",
        json={
            "email": "alex@example.com",
            "password": "123456",
            "phone_number": "+79991234567",
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "alex@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный email или пароль"
@pytest.mark.asyncio
async def test_get_current_user(client):
    await client.post(
        "/auth/register",
        json={
            "email": "alex@example.com",
            "password": "123456",
            "phone_number": "+79991234567",
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )

    login_response = await client.post(
        "/auth/login",
        json={
            "email": "alex@example.com",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200

    response = await client.get("/auth/me")

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "alex@example.com"
    assert data["phone_number"] == "+79991234567"
    assert data["first_name"] == "Алексей"
    assert data["last_name"] == "Фролов"
    assert "password" not in data
    assert "hashed_password" not in data
@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Токен отсутствует"
@pytest.mark.asyncio
async def test_logout_user(client):
    await client.post(
        "/auth/register",
        json={
            "email": "alex@example.com",
            "password": "123456",
            "phone_number": "+79991234567",
            "first_name": "Алексей",
            "last_name": "Фролов",
        },
    )

    login_response = await client.post(
        "/auth/login",
        json={
            "email": "alex@example.com",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200

    me_response_before_logout = await client.get("/auth/me")
    assert me_response_before_logout.status_code == 200

    logout_response = await client.post("/auth/logout")

    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Пользователь успешно вышел из системы"

    me_response_after_logout = await client.get("/auth/me")

    assert me_response_after_logout.status_code == 401
    assert me_response_after_logout.json()["detail"] == "Токен отсутствует"