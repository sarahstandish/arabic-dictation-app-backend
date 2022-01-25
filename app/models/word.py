from flask import current_app
from app import db
import random

class Word(db.Model):

    max_return_list_len = 10

    id = db.Column(db.Integer, primary_key=True)
    voweled_word = db.Column(db.String(50))
    unvoweled_word = db.Column(db.String(50))
    __tablename__ = 'words'

    def to_dict(self):
        return {
            "id": self.id,
            "voweled_word": self.voweled_word,
            "unvoweled_word": self.unvoweled_word,
            "word_to_pronounce": self.get_word_to_pronounce()
        }

    def get_word_to_pronounce(self):
        """
        Create a word with sukuun on the end of the word that can be pronounced by the Google text to speech API without tanween damma on the end

            U+0652 sukuun
            U+064B tanween fatha
        """

        acceptable_endings = [
            "\u0650", # kesra
            "\u064F", # damma
            "\u064E", # fatha
            "\u0652", # sukuun
            "\u064B", # tanween fatha
            "\u0627", # alif
            "\u0649" # alif maqsuura
            ]

        if self.voweled_word[-1] not in acceptable_endings:
            # append sukuun to the word and return it
            return self.voweled_word + "\u0652"

        return self.voweled_word

    @classmethod
    def get_randomized_list(cls, l):
        """
        Input: list of instances returned from the database
        Return ten random items from responses that generate more than ten responses
        Randomize lists that returned fewer than ten responses
        """
        # return the same list shuffled
        if len(l) <= cls.max_return_list_len:
            random.shuffle(l)
            return l

        # if the length of the list is greater than the desired return list size or greater, return that number of random items
        randomized_list = random.sample(l, cls.max_return_list_len)
        return randomized_list

    @classmethod
    def return_options_exhausted(cls, l):
        """
        Return whether or not the return list has exhausted the options returned from the database
        """
        return len(l) <= cls.max_return_list_len

    @staticmethod
    def get_letter_filter_array(letters):
        return list(letters)