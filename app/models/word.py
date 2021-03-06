from flask import current_app, abort, make_response, Response, jsonify
from app import db
import random
import hashlib

class Word(db.Model):

    # variable that determines the maximum number of database entries that will be returned
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
            "audio_file": Word.get_audio_url(self.voweled_word)
        }

    @staticmethod
    def get_audio_url(voweled_word):
        """
        Generate the url where the audio file for that word can be found.
        The file name is a hex digest of an md5 hash of the voweled version of the word.
        """
        file_name = hashlib.md5(bytes(voweled_word, 'utf-8')).hexdigest()
        base_url = "https://storage.googleapis.com/arabic-dictation-app/"
        audio_file_url = base_url + file_name
        return audio_file_url

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
    def more_words_available(cls, l):
        """
        Return whether or not the return list has exhausted the options returned from the database
        """
        return len(l) > cls.max_return_list_len

    @staticmethod
    def get_letter_string(letters):
        """
        Generate a string to be used in the SQL query.
        The SQL query will return only 
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
            "\u064B", # tanween fatha
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

    @staticmethod
    def row_proxy_to_dict(rowproxy):
        """
        Change a sqlalchemy RowProxy object to a dictionary.
        """

        return {
            "id": rowproxy['id'],
            "voweled_word": rowproxy['voweled_word'],
            "unvoweled_word": rowproxy['unvoweled_word'],
            "audio_file": Word.get_audio_url(rowproxy['voweled_word'])
        }

    @staticmethod
    def invalid_query_string_length(letters):

        """
        check if query string is at least three unique characters
        """
        # change to a set to de-dupe

        letters_set = set(list(letters))

        return len(letters_set) < 3

    def invalid_query_string_chars(letters):
        """
        Check if there are non-arabic characters in the query string
        """

        lowest_arabic_code_point = int('0600', 16)

        highest_arabic_code_point = int('06FF', 16)

        for char in letters:
            if ord(char) < lowest_arabic_code_point or ord(char) > highest_arabic_code_point:
                return True

        return False


        
