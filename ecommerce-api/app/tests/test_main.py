from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/register",
        json={"username": "url1999", "email": "uar1999@foxmail.com", "is_seller": True, "password": "123456"}
    )
    assert response.status_code == 200


def test_login_user():
    user_data = {"username": "admin", "email": "urr19890@foxmail.com", "is_seller": True, "password": "123456"}
    response = client.post("/users/login", json=user_data)

    json_str = json.loads(response.content)
    seller_token = json_str['access_token']

    response = client.get("/users/info", headers={"Authorization": f"Bearer " + seller_token+""})
    assert response.status_code == 200

    category_data = {"name": "Electric Tools3", "description": "Various electric tools"}
    response = client.post("/categories/create", json=category_data, headers={"Authorization": f"Bearer " + seller_token+""})
    assert response.status_code == 200


def test_get_products():
    response = client.get("/products/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product():
    user_data = {"username": "alice", "email": "usr1988@foxmail.com", "is_seller": True, "password": "123456"}
    product_data = {"Test Product": "Hexxx", "description": "OK11111", "price": 23.3, "category_id": 1, "stock": 10}
    # User login
    response = client.post("/users/login", json=user_data)
    assert response.status_code == 200

    json_str = json.loads(response.content)
    seller_token = json_str['access_token']
    response = client.post(
        "/products/create",
        json=product_data,
        headers={"Authorization": f"Bearer {seller_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"


