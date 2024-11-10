import pytest
from httpx import AsyncClient

from app.models import Role
from tests.factory.users import create_fake_user


@pytest.mark.asyncio
class TestUserEndpoints:
    @pytest.mark.parametrize("role", [Role.ADMIN, Role.MODERATOR])
    async def test_create_user(self, authenticated_client: AsyncClient, role: Role):
        """Test user creation"""
        fake_user = create_fake_user()
        response = await authenticated_client.post("/api/v1/users", json=fake_user)
        assert response.status_code == 201
        assert response.json()["username"] == fake_user["username"]
        assert "id" in response.json()

    @pytest.mark.parametrize("role", [Role.USER])
    async def test_unauthorized_create_user(
        self, authenticated_client: AsyncClient, role: Role
    ):
        """Test unauthorized user creation"""
        fake_user = create_fake_user()
        response = await authenticated_client.post("/api/v1/users", json=fake_user)
        assert response.status_code == 403

    @pytest.mark.parametrize("role", [Role.ADMIN, Role.MODERATOR])
    async def test_create_user_with_existing_username(
        self, authenticated_client: AsyncClient, role: Role
    ):
        """Test user creation with existing username"""
        fake_user = create_fake_user()
        await authenticated_client.post("/api/v1/users", json=fake_user)
        response = await authenticated_client.post("/api/v1/users", json=fake_user)
        assert response.status_code == 400

    @pytest.mark.parametrize("role", [Role.ADMIN, Role.USER, Role.MODERATOR])
    async def test_get_all_users(self, authenticated_client: AsyncClient, role: Role):
        """Test get all users with authorized access."""
        response = await authenticated_client.get("/api/v1/users")
        assert response.status_code == 200

    @pytest.mark.parametrize("role", [Role.ADMIN])
    async def test_get_user_by_id(self, authenticated_client: AsyncClient, role: Role):
        """Test get user by id with authorized access."""
        fake_user = create_fake_user()
        response = await authenticated_client.post("/api/v1/users", json=fake_user)
        user_id = response.json()["id"]
        response = await authenticated_client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    @pytest.mark.parametrize("role", [Role.ADMIN])
    async def test_search_users_by_username(
        self, authenticated_client: AsyncClient, role: Role
    ):
        """Test search users by username with authorized access."""
        fake_user = create_fake_user()
        response = await authenticated_client.post("/api/v1/users", json=fake_user)
        username = fake_user["username"]
        response = await authenticated_client.get(
            f"/api/v1/users/search/?query={username}"
        )
        assert response.status_code == 200
        assert response.json()[0]["username"] == username

    @pytest.mark.parametrize("role", [Role.ADMIN, Role.USER, Role.MODERATOR])
    async def test_get_me(self, authenticated_client: AsyncClient, role: Role):
        """Test get current user's information."""
        response = await authenticated_client.get("/api/v1/users/me")
        assert response.status_code == 200
        assert "username" in response.json()
        assert "role" in response.json()
