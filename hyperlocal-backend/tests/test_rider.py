import uuid


def test_rider_apply_verify_token_me(client):
    email = f"rider_{uuid.uuid4().hex[:8]}@example.com"
    body = {
        "email": email,
        "full_name": "Rider Demo",
        "phone": "9888888888",
        "aadhaar_last_four": "1234",
        "reason_to_join": "I want to deliver locally in Pune for extra income.",
    }
    a = client.post("/api/v1/riders/apply", json=body)
    assert a.status_code == 200
    rid = a.json()["id"]

    v = client.post("/api/v1/riders/verify", json={"rider_id": rid, "approve": True})
    assert v.status_code == 200
    assert v.json()["status"] == "verified"

    t = client.post(f"/api/v1/riders/{rid}/token")
    assert t.status_code == 200
    token = t.json()["access_token"]

    me = client.get("/api/v1/riders/me/status", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email.lower()
