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


def test_get_words_one_saved_word(client, add_one_word):
    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    words = response_body['words']
    assert response_body["more_words_available"] == False
    assert len(words) == 1
    assert words[0]["voweled_word"] == "ثُبوت"
    assert words[0]["unvoweled_word"] == "ثبوت"
    assert words[0]["word_to_pronounce"] == "ثُبوتْ"

def test_get_words_eleven_saved_words(client, add_eleven_words):

    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["more_words_available"] == True
    words = response_body["words"]
    assert len(words) == MAX_RETURN_LIST_LEN
    for word in words:
        assert word["word_to_pronounce"][-1] in ACCEPTABLE_WORD_ENDINGS
        for char in word["unvoweled_word"]:
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
    assert response_body["more_words_available"] == False
    words = response_body["words"]
    assert len(words) == 1
    assert words[0]["voweled_word"] == "ثَبَتَ"
    assert words[0]["unvoweled_word"] == "ثبت"
    assert words[0]["word_to_pronounce"] == "ثَبَتَ"

def test_get_words_longer_query_param(client, add_eleven_words):

    """
    Four words should be returned
    """
    
    # Act
    response = client.get("/words?letters=انوتبث")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response_body["more_words_available"] == False
    words = response_body["words"]
    assert len(words) == 3
    for word in words:
        assert word["word_to_pronounce"][-1] in ACCEPTABLE_WORD_ENDINGS
        for char in word["unvoweled_word"]:
                assert char not in DIACRITICS



