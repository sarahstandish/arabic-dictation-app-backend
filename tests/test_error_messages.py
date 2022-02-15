from app.models.word import Word

def test_get_words_no_saved_words(client):
    """
    Tests what happens when the database is empty, identical to behavior if there are no results returned.
    """
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == { "message": "No results matched your search." }

def test_get_words_query_param_too_short(client, add_three_words):
    """
    Return an error if query param is fewer than three characters
    """

    # Act
    response = client.get("/words?letters=من")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Query string must contain at least three valid characters."}

def test_get_words_query_param_has_repeated_character(client, add_three_words):
    """
    Return an error if query param is fewer than three unique characters
    """

    # Act
    response = client.get("/words?letters=ممم")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Query string must contain at least three valid characters."}

def test_get_words_query_param_has_non_arabic_character(client, add_three_words):
    """
    Return an error if query param contains a non-Arabic character
    """

    # Act
    response = client.get("/words?letters=hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message" : "Invalid characters."}