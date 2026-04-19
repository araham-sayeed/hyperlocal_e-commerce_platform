import uuid


def test_orders_place_and_fetch(client):
    email = f"o_shop_{uuid.uuid4().hex[:8]}@example.com"
    assert (
        client.post(
            "/api/v1/shop-owners/register",
            json={
                "email": email,
                "password": "password123",
                "full_name": "O Owner",
                "shop_name": "O Shop",
                "phone": "9111111111",
                "latitude": 18.52,
                "longitude": 73.85,
            },
        ).status_code
        == 200
    )
    st = client.post("/api/v1/shop-owners/login", json={"email": email, "password": "password123"})
    shop_tok = st.json()["access_token"]

    cats = client.get("/api/v1/catalog/categories")
    assert cats.status_code == 200
    cat_id = cats.json()[0]["id"]
    subs = client.get(f"/api/v1/catalog/categories/{cat_id}/subcategories")
    sub_id = subs.json()[0]["id"]

    pr = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {shop_tok}"},
        json={
            "subcategory_id": sub_id,
            "name": "Demo SKU",
            "description": "For tests",
            "price": "199.00",
            "stock_quantity": 5,
        },
    )
    assert pr.status_code == 200
    pid = pr.json()["id"]

    phone = f"92{uuid.uuid4().int % 10_000_000_000:010d}"
    client.post("/api/v1/customers/otp/send", json={"phone": phone})
    ct = client.post("/api/v1/customers/otp/verify", json={"phone": phone, "code": "424242"}).json()[
        "access_token"
    ]
    shop_id = client.get("/api/v1/shop-owners/me", headers={"Authorization": f"Bearer {shop_tok}"}).json()["id"]

    order = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {ct}"},
        json={
            "shop_owner_id": shop_id,
            "lines": [{"product_id": pid, "quantity": 2}],
            "delivery_latitude": 18.51,
            "delivery_longitude": 73.80,
        },
    )
    assert order.status_code == 200
    oid = order.json()["id"]

    got = client.get(f"/api/v1/orders/{oid}", headers={"Authorization": f"Bearer {ct}"})
    assert got.status_code == 200
    assert got.json()["items"][0]["product_id"] == pid
