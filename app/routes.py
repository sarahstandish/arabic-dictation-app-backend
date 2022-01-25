from flask import Blueprint, json, jsonify, request, make_response
from .models.word import Word
from app import db

words_bp = Blueprint("words", __name__, url_prefix="/words")

@words_bp.route("", methods=["GET"])
def handle_words():

    letters = request.args.get("letters")

    if letters:
        letters = Word.get_letter_filter_array(letters)
        return { "message" : f"letters {letters} received"}
    
    words = Word.query.all()

    words = Word.get_randomized_list(words)

    return jsonify([word.to_dict() for word in words])
