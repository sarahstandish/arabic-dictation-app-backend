from app.models.word import Word

def test_get_word_by_id_one_saved_word(client, add_one_word):
    # Act
    response = client.get("/words/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1