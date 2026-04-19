def test_chat_session_and_message(client):
    s = client.post("/api/v1/chat/sessions", json={"title": "Support"})
    assert s.status_code == 200
    sid = s.json()["id"]
    m = client.post(f"/api/v1/chat/sessions/{sid}/messages", json={"content": "Hello"})
    assert m.status_code == 200
    assert "assistant_message" in m.json()
