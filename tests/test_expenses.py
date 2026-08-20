import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# Use a temporary in-memory SQLite database instead of development data.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    # Make the API use the test database during this test.
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_expense_crud(client):
    expense_data = {
        "description": "Groceries",
        "amount": "45.75",
        "category": "Food",
        "expense_date": "2026-08-20",
    }

    create_response = client.post("/expenses", json=expense_data)

    assert create_response.status_code == 201
    expense_id = create_response.json()["id"]

    get_response = client.get(f"/expenses/{expense_id}")

    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Groceries"

    updated_data = {
        "description": "Weekly groceries",
        "amount": "52.25",
        "category": "Food",
        "expense_date": "2026-08-20",
    }

    update_response = client.put(
        f"/expenses/{expense_id}",
        json=updated_data,
    )

    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Weekly groceries"

    delete_response = client.delete(f"/expenses/{expense_id}")

    assert delete_response.status_code == 204

    missing_response = client.get(f"/expenses/{expense_id}")

    assert missing_response.status_code == 404