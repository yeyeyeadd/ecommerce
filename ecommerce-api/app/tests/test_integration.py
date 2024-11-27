from fastapi.testclient import TestClient
import json

from app.main import app

client = TestClient(app)


def test_order_creation():
    user_data = {"username": "dev1999", "email": "usr1988@foxmail.com", "is_seller": True, "password": "123456"}
    product_data = {"name": "Phone4", "description": "Blue ruler222", "price": 5.99, "category_id": 2, "stock": 20}
    order_data = {"items": [{"product_id": 5, "quantity": 1}, {"product_id": 6, "quantity": 1}]}

    # Register user
    # response = client.post("/users/register", json=user_data)
    # assert response.status_code == 200

    # User login
    response = client.post("/users/login", json=user_data)
    assert response.status_code == 200

    json_str = json.loads(response.content)
    seller_token = json_str['access_token']

    # User info
    response = client.get("/users/info", headers={"Authorization": f"Bearer " + seller_token+""})
    assert response.status_code == 200

    # Add product
    # response = client.post("/products/create", json=product_data, headers={"Authorization": f"Bearer " + seller_token+""})
    # assert response.status_code == 200

    # Add order
    response = client.post("/orders/create", json=order_data, headers={"Authorization": f"Bearer " + seller_token+""})
    assert response.status_code == 200

