from get_audio_file import *
from upload_file import *
from get_word_to_pronounce import *
import os

def create_audio_file_upload_word(voweled_word):

    word_to_pronounce = get_word_to_pronounce(voweled_word)

    file_name = hashlib.md5(bytes(voweled_word, 'utf-8')).hexdigest()

    audio_file_loc = f"./text-processing/audio_files/{file_name}.mp3"

    get_audio_file(word_to_pronounce, audio_file_loc)

    bucket_name = "arabic-dictation-app"

    upload_blob(bucket_name, audio_file_loc, file_name)

    os.remove(audio_file_loc)