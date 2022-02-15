import os
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess

def get_audio_file_aws_polly(word_to_pronounce, file_destination):
    """
    Upload a piece of text to AWS Polly, get back an audio file with that text as audio
    """

    # create a client using the credentials and region defined in [adminuser]
    session = Session(profile_name="adminuser")
    polly = session.client("polly")

    try:
        # request speech synthesis
        response = polly.synthesize_speech(Text=word_to_pronounce, OutputFormat="mp3", VoiceId="Zeina")
    except (BotoCoreError, ClientError) as error:
        print("Error with word", word_to_pronounce)
        print(error)
        sys.exit(-1)

    # access the audio stream from the resposne
    if "AudioStream" in response:
        # note: closing the stream is important because the service throttles
        # on the number of parallel connections
        # Here we are using contextlib.closing to ensure the close method of the strea object
        # will be called automatically at the end of the with statement's scope
        with closing(response["AudioStream"]) as stream:
            # output = os.path.join(gettempdir(), "speech.mp3")
            output = file_destination

            try:
                # open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                print(f"Output file for {word_to_pronounce} at {output}")


            except IOError as error:
                # could not write to file, exit gracefullly
                print("Issue with", word_to_pronounce)
                print(error)
                sys.exit(-1)

    else:
        # the response didn't contain audio data, exit gracefully
        print("Could not stream audio for", word_to_pronounce)
        sys.exit(-1)

