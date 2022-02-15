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
    """
    Test return when database contains only one word.
    Expected behavior:
    - one word is returned, with a voweled and unvoweled version
    - no more words are available
    - audio file location is returned, where audio file name is a hexdigest of an md5 hash of the voweled version of the word
    """
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
    assert words[0]["audio_file"] == "https://storage.googleapis.com/arabic-dictation-app/f04974d81a18d14b05d895c192c5b6d0"

def test_get_words_eleven_saved_words(client, add_eleven_words):

    """
    Test return when database contains only one word.
    Expected behavior:
    - the number of words returned matches the maximum length of a returned list of words, as set by the API
    - more words matching the parameters are available
    - unvoweled word fields do not contain diacritics
    """

    # Act
    response = client.get("/words")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["more_words_available"] == True
    words = response_body["words"]
    assert len(words) == MAX_RETURN_LIST_LEN
    for word in words:
        for char in word["unvoweled_word"]:
                assert char not in DIACRITICS

def test_get_words_query_param_tha_ba_ta(client, add_eleven_words):

    """
    Test return when query string searches for words containing only ث ب ت and only one word matches in database
    Expected behavior:
    - one word is returned, with a voweled and unvoweled version
    - the word returned only contains the letters ث ب ت
    - no more words are available
    - audio file location is returned, where audio file name is a hexdigest of an md5 hash of the voweled version of the word
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
    assert words[0]["audio_file"] == "https://storage.googleapis.com/arabic-dictation-app/84d7dc8ded0e456a5267b756bbf6a1d6"


def test_get_words_longer_query_param(client, add_eleven_words):

    """
    Test return when query string searches for words containing only ث ب ت and only one word matches in database
    Expected behavior:
    - four words are returned
    - the word returned only contains the letters ا ن و ت ب ث
    - no more words are available
    - unvoweled word fields do not contain diacritics
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
        for char in word["unvoweled_word"]:
                assert char not in DIACRITICS



