from encodings import utf_8
from flask import Blueprint, json, jsonify, request, make_response
import sqlalchemy
from .models.word import Word
from app import db
from flask_cors import cross_origin

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
