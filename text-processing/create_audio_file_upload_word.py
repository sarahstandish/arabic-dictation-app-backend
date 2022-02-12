from get_audio_file_google_tts import *
from get_audio_file_aws_polly import *
from upload_file import *
from get_word_to_pronounce import *
import os

def create_audio_file_upload_word(voweled_word):

    # only necessary with google tts
    # word_to_pronounce = get_word_to_pronounce(voweled_word)

    file_name = hashlib.md5(bytes(voweled_word, 'utf-8')).hexdigest()

    audio_file_loc = f"./text-processing/audio_files/{file_name}.mp3"

    # get_audio_file_google_tts(word_to_pronounce, audio_file_loc)
    get_audio_file_aws_polly(voweled_word, audio_file_loc)

    bucket_name = "arabic-dictation-app"

    upload_blob(bucket_name, audio_file_loc, file_name)

    os.remove(audio_file_loc)

create_audio_file_upload_word("طِبّ")