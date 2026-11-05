from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi.testclient import TestClient

from app.db import get_session
from app.main import app


class FakeSession:
    """Stands in for a database session, so these tests need no real database."""

    def __init__(self, error: Exception | None = None) -> None:
        self.error = error

    async def execute(self, _statement: object) -> None:
        if self.error:
            raise self.error


def use_session(session: FakeSession) -> None:
    async def override() -> AsyncIterator[FakeSession]:
        yield session

    # Swaps a dependency for the duration of a test, without patching any imports.
    app.dependency_overrides[get_session] = override


@pytest.fixture(autouse=True)
def reset_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_reports_database_up() -> None:
    use_session(FakeSession())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": True}


def test_reports_database_down_and_still_returns_200() -> None:
    use_session(FakeSession(error=ConnectionError("database unreachable")))

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": False}
