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

        sql_query = sqlalchemy.text(f"SELECT * FROM words WHERE unvoweled_word NOT SIMILAR TO '{similar_to_string}'")
        words = db.session.execute(sql_query).fetchall()
        # result is a list of rowproxy items
        # for r in result:
        #     # can be accessed via keys r['voweled_word']
        #     print(type(r))
        #     print(r.items())
        #     print(r['voweled_word'])
        words = Word.get_randomized_list(words)
        return jsonify([Word.row_proxy_to_dict(word) for word in words])

    else:
        words = Word.query.all()

        words = Word.get_randomized_list(words)

        return jsonify([word.to_dict() for word in words])
