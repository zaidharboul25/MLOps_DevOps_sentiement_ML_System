def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "SentimentAI" in response.text
    assert "version 1.0" in response.text.lower()


def test_dashboard_uses_saved_data(client):
    client.post("/api/texts", json={"content": "Dashboard test"})
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Dashboard test" in response.text


def test_web_form_stores_text_and_detail_shows_confirmation(client):
    response = client.post("/texts/new", data={"content": "Une idée depuis le formulaire"}, follow_redirects=True)
    assert response.status_code == 200
    assert "bien été enregistré" in response.text
    assert "Une idée depuis le formulaire" in response.text
