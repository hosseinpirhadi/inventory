from src.main import app
from fastapi.testclient import TestClient
from faker import Faker

client = TestClient(app)


def test_read_main():
    response = client.get("/person")
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

def test_create_person():
    fake = Faker()
    name = fake.name()
    response = client.post(
                            "/person",
                            json={"name": name,
                                "password": "password"},
                        )

    assert response.status_code == 201

    response_json = response.json()
    assert "id" in response_json
    assert response_json["name"] == name.lower()