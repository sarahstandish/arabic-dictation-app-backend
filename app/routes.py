from flask import Blueprint, json, jsonify, request, make_response
from .models.word import Word
from app import db

words_bp = Blueprint("words", __name__, url_prefix="/words")

@words_bp.route("", methods=["GET"])
def handle_words():
    pass