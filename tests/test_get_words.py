from app.models.word import Word

def test_get_words_no_saved_words(client):
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []