import pytest
from httpx import AsyncClient

from app.models import Role
from tests.factory.users import create_fake_user


@pytest.mark.parametrize("role", [Role.ADMIN, Role.MODERATOR])
@pytest.mark.asyncio
async def test_create_user(
    authenticated_client: AsyncClient, role: Role  # noqa: ARG001
):
    """Test user creation"""
    fake_user = create_fake_user()
    response = await authenticated_client.post("/api/v1/users", json=fake_user)
    assert response.status_code == 201
    assert response.json()["username"] == fake_user["username"]
    assert "id" in response.json()


@pytest.mark.parametrize("role", [Role.USER])
@pytest.mark.asyncio
async def test_unauthorized_create_user(
    authenticated_client: AsyncClient, role: Role  # noqa: ARG001
):  # noqa: ARG001
    """Test unauthorized user creation"""
    fake_user = create_fake_user()
    response = await authenticated_client.post("/api/v1/users", json=fake_user)
    assert response.status_code == 403


@pytest.mark.parametrize("role", [Role.ADMIN, Role.MODERATOR])
@pytest.mark.asyncio
async def test_create_user_with_existing_username(
    authenticated_client: AsyncClient, role: Role  # noqa: ARG001
):
    """Test user creation with existing username"""
    fake_user = create_fake_user()
    await authenticated_client.post("/api/v1/users", json=fake_user)
    response = await authenticated_client.post("/api/v1/users", json=fake_user)
    assert response.status_code == 400


@pytest.mark.parametrize("role", [Role.ADMIN, Role.USER, Role.MODERATOR])
@pytest.mark.asyncio
async def test_get_all_users(
    authenticated_client: AsyncClient, role: Role  # noqa: ARG001
):
    """Test get all users with authorized access."""
    response = await authenticated_client.get("/api/v1/users")
    assert response.status_code == 200


@pytest.mark.parametrize("role", [Role.ADMIN, Role.USER, Role.MODERATOR])
@pytest.mark.asyncio
async def test_get_me(authenticated_client: AsyncClient, role: Role):  # noqa: ARG001
    """Test get current user's information."""
    response = await authenticated_client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert "username" in response.json()
    assert "role" in response.json()
