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
    def get_letter_string(letters):
        """
        Letters is a string from the url query params.
        Change these letters to a set.
        Subtract that set from the set of all possible letters.
        Transform the set of all remaining letters to a string in form "%(letter|letter|letter)%" etc. Return it.
        """
        all_letters = {
            "\u0621", # independent hamza
            "\u0622", # alif medda
            "\u0623", # alif with hamza on top
            "\u0625", # alif with hamza on bottom
            "\u0624", # waw with hamza on top
            "\u0626", # yaa with hamza on top
            "\u0627", # alif
            "\u0628", # baa
            "\u0629", # taa marbuuta
            "\u062A", # taa
            "\u062B", # thaa
            "\u062C", # jeem
            "\u062D", # Haa
            "\u062E", # khaa
            "\u062F", # daal
            "\u0630", # dhaal,
            "\u0631", # raa,
            "\u0632", # zay
            "\u0633", # seen
            "\u0634", # sheen
            "\u0635", # saad
            "\u0636", # daad
            "\u0637", # taa
            "\u0638", # dhaa
            "\u0639", # ayn
            "\u063A", # ghayn
            "\u0641", # faa
            "\u0642", # qaaf
            "\u0643", # kaaf
            "\u0644", # laam
            "\u0645", # meem
            "\u0646", # nuun
            "\u0647", # haa
            "\u0648", # waaw
            "\u064A", # yaa
            "\u0649", # alif maqsuura
        }
        query_param_letters = set(list(letters))

        letters_to_filter_out = all_letters - query_param_letters

        letters_to_filter_out = list(letters_to_filter_out)

        similar_to_string = "%("

        for char in letters_to_filter_out:
            similar_to_string += char
            similar_to_string += "|"

        # remove the final pipe character
        similar_to_string = similar_to_string[:-1]
        similar_to_string += ")%"

        return similar_to_string