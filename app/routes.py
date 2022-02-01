from encodings import utf_8
from pydoc import text
from flask import Blueprint, json, jsonify, request, make_response
import sqlalchemy
from .models.word import Word
from app import db
from flask_cors import cross_origin
from google.cloud import texttospeech
import base64

words_bp = Blueprint("words", __name__, url_prefix="/words")

@words_bp.route("", methods=["GET"])
@cross_origin() # enable CORS
def handle_words():

    letters = request.args.get("letters")

    # if query param found, filter by letters in query param value
    if letters:

        # check if query string is valid
        if Word.invalid_query_string_length(letters):
            return { "message" : "Query string must contain at least three valid characters."}, 400
        
        # check if the string has non-Arabic characters
        if Word.invalid_query_string_chars(letters):
            return { "message" : "Invalid characters"}, 400

        # get string to pass to sql query
        similar_to_string = Word.get_letter_string(letters)

        # form sql query
        sql_query = sqlalchemy.text(f"SELECT * FROM words WHERE unvoweled_word NOT SIMILAR TO '{similar_to_string}'")

        # execute query
        words = db.session.execute(sql_query).fetchall()

        # create a list of dictionaries
        words = [Word.row_proxy_to_dict(word) for word in words]

    # if no query param found, return all words
    else:
        # fetch words
        words = Word.query.all()
        
        # create a list of dictionaries
        words = [word.to_dict() for word in words]

    # select randomly from the list
    more_words_available = Word.more_words_available(words)
    words = Word.get_randomized_list(words)

    if not words:
        return jsonify({ "message": "no results matched your search" }), 404

    return jsonify({
        "more_words_available": more_words_available,
        "words": words
    })

@words_bp.route("/<word_id>", methods=["GET"])
@cross_origin()
def handle_word(word_id):
    
    word = Word.query.get(word_id)

    word_to_pronounce = word.get_word_to_pronounce()

    # instantiate a client
    client = texttospeech.TextToSpeechClient()

    # set the text to be synthesized
    input = texttospeech.SynthesisInput(text=word_to_pronounce)

    # the voice I want to speak the content
    voice = texttospeech.VoiceSelectionParams(
        language_code="ar-XA", name="ar-XA-Wavenet-B"
    )

    # the type of audio I want returned
    # let's go with mp3 for now and maybe change that later if need be
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # perform the text-to-speech request
    response = client.synthesize_speech(input=input, voice=voice, audio_config=audio_config)
    print("Response type is", type(response))
    # b64_encoded_str = base64.b64encode(response.audio_content)
    # print(b64_encoded_str)

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    return jsonify({"audio_content": str(response.audio_content)})