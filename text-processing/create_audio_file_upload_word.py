from get_audio_file import *
from upload_file import *
from get_word_to_pronounce import *

def create_audio_file_upload_word(word):

    word_to_pronounce = get_word_to_pronounce(word)

    file_name = hashlib.md5(bytes(word, 'utf-8')).hexdigest()

    audio_file_loc = f"./text-processing/audio_files/{file_name}.mp3"

    get_audio_file(word_to_pronounce, audio_file_loc)

    bucket_name = "arabic-dictation-app"

    upload_blob(bucket_name, audio_file_loc, file_name)