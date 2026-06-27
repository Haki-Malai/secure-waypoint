import base64
from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.models import User
from core.config import config


@pytest.mark.asyncio
class TestTokenEndpoints:
    async def _login(self, client: AsyncClient, username: str, password: str):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        return await client.post("/api/v1/tokens", headers=headers)

    async def test_login(self, client: AsyncClient, user: User):
        response = await self._login(client, user.username, "password")
        assert response.status_code == 200

    async def test_refresh_token_success(self, client: AsyncClient, user: User):
        token_response = await self._login(client, user.username, "password")

        refresh_token = token_response.json()["refresh_token"]
        access_token = token_response.json()["access_token"]

        client.headers.update({"Authorization": f"Bearer {access_token}"})

        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": refresh_token}
        )
        assert refresh_response.status_code == HTTP_200_OK
        assert "access_token" in refresh_response.json()

    async def test_refresh_token_rejects_access_token_as_refresh(
        self, client: AsyncClient, user: User
    ):
        token_response = await self._login(client, user.username, "password")

        access_token = token_response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {access_token}"})

        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": access_token}
        )

        assert refresh_response.status_code == HTTP_401_UNAUTHORIZED

    async def test_refresh_token_rejects_token_for_different_user(
        self, client: AsyncClient, user: User, db_session: AsyncSession
    ):
        other_user = User(username="otheruser", password="password")
        db_session.add(other_user)
        await db_session.commit()

        user_token_response = await self._login(client, user.username, "password")
        other_token_response = await self._login(
            client, other_user.username, "password"
        )

        access_token = user_token_response.json()["access_token"]
        refresh_token = other_token_response.json()["refresh_token"]
        client.headers.update({"Authorization": f"Bearer {access_token}"})

        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == HTTP_401_UNAUTHORIZED

    async def test_refresh_token_rejects_expired_access_token(
        self, client: AsyncClient, user: User
    ):
        token_response = await self._login(client, user.username, "password")

        refresh_token = token_response.json()["refresh_token"]
        expired_access_token = jwt.encode(
            {
                "user_id": user.id,
                "token_type": "access",
                "exp": datetime.now(UTC) - timedelta(minutes=1),
            },
            config.SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        client.headers.update({"Authorization": f"Bearer {expired_access_token}"})

        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == HTTP_401_UNAUTHORIZED

    async def test_refresh_token_rejects_deleted_user(
        self, client: AsyncClient, user: User, db_session: AsyncSession
    ):
        token_response = await self._login(client, user.username, "password")

        refresh_token = token_response.json()["refresh_token"]
        access_token = token_response.json()["access_token"]
        await db_session.delete(user)
        await db_session.commit()
        client.headers.update({"Authorization": f"Bearer {access_token}"})

        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == HTTP_401_UNAUTHORIZED

    async def test_refresh_token_unauthorized(self, client: AsyncClient):
        refresh_response = await client.put(
            "/api/v1/tokens", json={"refresh_token": "invalid_or_expired_refresh_token"}
        )
        assert refresh_response.status_code == HTTP_401_UNAUTHORIZED
