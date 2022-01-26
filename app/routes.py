from encodings import utf_8
from flask import Blueprint, json, jsonify, request, make_response
import sqlalchemy
from .models.word import Word
from app import db

words_bp = Blueprint("words", __name__, url_prefix="/words")

@words_bp.route("", methods=["GET"])
def handle_words():

    letters = request.args.get("letters")

    if letters:
        similar_to_string = Word.get_letter_string(letters)

        sql_query = sqlalchemy.text(f"select * from words where unvoweled_word not similar to '{similar_to_string}'")
        result = db.session.execute(sql_query)
        for r in result:
            print(r)

        return { "message" : f"letters {similar_to_string} received"}


    else:
        words = Word.query.all()
        print(type(words))
        print(type(words[0]))

    words = Word.get_randomized_list(words)

    return jsonify([word.to_dict() for word in words])
