import uuid


def test_customer_otp_flow(client):
    phone = f"91{uuid.uuid4().int % 10_000_000_000:010d}"
    s = client.post("/api/v1/customers/otp/send", json={"phone": phone})
    assert s.status_code == 200
    v = client.post("/api/v1/customers/otp/verify", json={"phone": phone, "code": "424242"})
    assert v.status_code == 200
    token = v.json()["access_token"]
    me = client.get("/api/v1/customers/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["phone"] == phone
