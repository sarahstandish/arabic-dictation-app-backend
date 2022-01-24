from flask import current_app
from app import db

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voweled_word = db.Column(db.String(50))
    unvoweled_word = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "voweled_word": self.voweled_word,
            "unvoweled_word": self.unvoweled_word
        }