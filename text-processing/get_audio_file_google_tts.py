from google.cloud import texttospeech
import hashlib

def get_audio_file_google_tts(word_to_pronounce, file_destination):
    
    # instantiate a client
    client = texttospeech.TextToSpeechClient()

    # set the text to be synthesized
    input = texttospeech.SynthesisInput(text=word_to_pronounce)

    # the voice I want to speak the content
    voice = texttospeech.VoiceSelectionParams(
        language_code="ar-XA", name="ar-XA-Wavenet-B"
    )

    # the type of audio I want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # perform the text-to-speech request
    response = client.synthesize_speech(input=input, voice=voice, audio_config=audio_config)

    with open(file_destination, "wb") as out:
        out.write(response.audio_content)
