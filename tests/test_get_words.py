from app.models.word import Word

MAX_RETURN_LIST_LEN = 10

DIACRITICS = [
    "\u0650", # kesra
    "\u064F", # damma
    "\u064E", # fatha
    "\u0651", # shadda
    "\u0652", # sukuun
    "\u0670", # dagger alif
    "\u064B" # tanween fatha
    ]

ACCEPTABLE_WORD_ENDINGS = [
    "\u0650", # kesra
    "\u064F", # damma
    "\u064E", # fatha
    "\u0652", # sukuun
    "\u064B", # tanween fatha
    "\u0627", # alif
    "\u0649" # alif maqsuura
    ]

def test_get_words_no_saved_words(client):
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_words_one_saved_word(client, add_one_word):
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["voweled_word"] == "ثُبوت"
    assert response_body[0]["unvoweled_word"] == "ثبوت"
    assert response_body[0]["word_to_pronounce"] == "ثُبوتْ"

def test_get_words_eleven_saved_words(client, add_eleven_words):

    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == MAX_RETURN_LIST_LEN
    for response in response_body:
        assert response["word_to_pronounce"][-1] in ACCEPTABLE_WORD_ENDINGS
        for char in response["unvoweled_word"]:
                assert char not in DIACRITICS

def test_get_words_query_param_tha_ba_ta(client, add_eleven_words):

    """
    Only one word should be returned
    """
    
    # Act
    response = client.get("/words?letters=تبث")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["voweled_word"] == "ثَبَتَ"
    assert response_body[0]["unvoweled_word"] == "ثبت"
    assert response_body[0]["word_to_pronounce"] == "ثَبَتَ"

def test_get_words_longer_query_param(client, add_eleven_words):

    """
    Four words should be returned
    """
    
    # Act
    response = client.get("/words?letters=انوتبث")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    for response in response_body:
        assert response["word_to_pronounce"][-1] in ACCEPTABLE_WORD_ENDINGS
        for char in response["unvoweled_word"]:
                assert char not in DIACRITICS

