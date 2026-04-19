import uuid

def test_shop_owner_register_login_me(client):
    email = f"shop_{uuid.uuid4().hex[:8]}@example.com"
    reg = {
        "email": email,
        "password": "password123",
        "full_name": "Demo Owner",
        "shop_name": "Demo Shop",
        "phone": "9999999999",
        "latitude": 18.5074,
        "longitude": 73.8077,
    }
    r = client.post("/api/v1/shop-owners/register", json=reg)
    assert r.status_code == 200
    assert r.json()["email"] == email.lower()

    login = client.post("/api/v1/shop-owners/login", json={"email": email, "password": "password123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/api/v1/shop-owners/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["shop_name"] == "Demo Shop"
