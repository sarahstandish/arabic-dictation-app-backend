import csv
from create_audio_file_upload_word import *

"""
Take vocabulary words from a CSV file 
Create an audio file
And upload it to the database
"""

source_file = "text-processing/voweled-and-unvoweled-words.csv"

def create_and_upload_all_words(source_file):

    with open(source_file, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        word_set = set()
        for row in reader:
            voweled_word = row["\ufeffvoweled_word"]
            if voweled_word not in word_set:
                create_audio_file_upload_word(voweled_word)
                word_set.add(voweled_word)

    csvfile.close()

create_and_upload_all_words(source_file)

