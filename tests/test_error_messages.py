from app.models.word import Word

def test_get_words_no_saved_words(client):
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == { "message": "No results matched your search." }

def test_get_words_query_param_too_short(client, add_three_words):
    """
    Return an error if query param is fewer than three letters
    """

    # Act
    response = client.get("/words?letters=من")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Query string must contain at least three valid characters."}

def test_get_words_query_param_has_repeated_character(client, add_three_words):
    """
    Return an error if query param is fewer than three letters
    """

    # Act
    response = client.get("/words?letters=ممم")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Query string must contain at least three valid characters."}

def test_get_words_query_param_has_non_arabic_character(client, add_three_words):
    """
    Return an error if query param is fewer than three letters
    """

    # Act
    response = client.get("/words?letters=hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Invalid characters."}