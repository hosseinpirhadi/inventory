from src.main import app
from fastapi.testclient import TestClient
from faker import Faker
import requests

client = TestClient(app)


def test_get_product():
    response = client.get("/product")
    assert response.status_code == 200


def create_access_token():
    fake = Faker()
    name = fake.name()
    client.post(
                "/person",
                json={"name": name, "password": "password"},
            )

    response = client.post(
                '/token',
                data={"username": name, "password": "password"},
                )

    return response.json()

def test_create_product():
    response = create_access_token()
    bearer_token = response['access_token']
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    fake = Faker()
    product_name = fake.word()
    response = client.post(
                            "/product",
                            headers=headers,
                            json={"name": product_name}
                        )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["name"] == product_name
