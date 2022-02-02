from google.cloud import texttospeech
from get_word_to_pronounce import *
import hashlib

def get_audio_file(word):
    
    # instantiate a client
    client = texttospeech.TextToSpeechClient()

    text = get_word_to_pronounce(word)

    # set the text to be synthesized
    input = texttospeech.SynthesisInput(text=text)

    # the voice I want to speak the content
    voice = texttospeech.VoiceSelectionParams(
        language_code="ar-XA", name="ar-XA-Wavenet-B"
    )

    file_code = hashlib.md5(bytes(word, 'utf-8')).hexdigest()
    

    # the type of audio I want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # perform the text-to-speech request
    response = client.synthesize_speech(input=input, voice=voice, audio_config=audio_config)

    with open(f"{file_code}.mp3", "wb") as out:
        out.write(response.audio_content)
