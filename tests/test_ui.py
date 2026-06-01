import pytest


@pytest.mark.asyncio
async def test_login_page_available(client):
    response = await client.get("/ui/login")

    assert response.status_code == 200
    assert "Вход в систему" in response.text


@pytest.mark.asyncio
async def test_dashboard_page_available(client):
    response = await client.get("/ui")

    assert response.status_code == 200
    assert "Панель управления" in response.text


@pytest.mark.asyncio
async def test_static_css_available(client):
    response = await client.get("/static/css/style.css")

    assert response.status_code == 200
    assert "body" in response.text


@pytest.mark.asyncio
async def test_static_js_available(client):
    response = await client.get("/static/js/ui.js")

    assert response.status_code == 200
    assert "DOMContentLoaded" in response.text