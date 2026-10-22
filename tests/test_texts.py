from fastapi.testclient import TestClient

from app.main import create_app


def test_create_and_list_text(client):
    response = client.post("/api/texts", json={"content": "Une première note."})
    assert response.status_code == 201
    entry = response.json()
    assert entry["content"] == "Une première note."
    assert client.get("/api/texts").json()[0]["id"] == entry["id"]


def test_reject_blank_text(client):
    assert client.post("/api/texts", json={"content": "  \n "}).status_code == 422


def test_reject_text_over_limit(client):
    assert client.post("/api/texts", json={"content": "x" * 5001}).status_code == 422


def test_get_existing_and_missing_text(client):
    created = client.post("/api/texts", json={"content": "À retrouver"}).json()
    assert client.get(f"/api/texts/{created['id']}").json()["content"] == "À retrouver"
    assert client.get("/api/texts/9999").status_code == 404


def test_delete_text(client):
    created = client.post("/api/texts", json={"content": "À supprimer"}).json()
    assert client.delete(f"/api/texts/{created['id']}").status_code == 204
    assert client.get(f"/api/texts/{created['id']}").status_code == 404


def test_data_persists_across_app_instances(tmp_path):
    database = tmp_path / "persistent-test.db"
    with TestClient(create_app(database)) as client:
        created = client.post("/api/texts", json={"content": "Toujours là"}).json()
    with TestClient(create_app(database)) as client:
        assert client.get(f"/api/texts/{created['id']}").json()["content"] == "Toujours là"
