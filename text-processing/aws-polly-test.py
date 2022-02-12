import os
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir


# create a client using the credentials and region defined in [adminuser]
session = Session(profile_name="adminuser")
polly = session.client("polly")

try:
    # request speech synthesis
    response = polly.synthesize_speech(Text="مرحبا يا عالم", OutputFormat="mp3", VoiceId="Zeina")
except (BotoCoreError, ClientError) as error:
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
        output = "./text-processing/audio_files/polly-test.mp3"
        print("Output file at", output)

        try:
            # open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())

        except IOError as error:
            # could not write to file, exit gracefullly
            print(error)
            sys.exit(-1)

else:
    # the response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# play the audio using the platform's default player
if sys.platform == 'win32':
    os.startfile(output)

else: 
    # words on mac
    opener = "open" if sys.platform == 'darwin' else "xdg-open"
    subprocess.call([opener, output])
