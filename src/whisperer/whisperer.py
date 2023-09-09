import openai
import os

class Whisperer():
    def __init__(self, audio_filename) -> None:
        self.audio_file = open(audio_filename, "rb")
        openai.api_key = open(os.getcwd() + "/whisperer/api_key.txt", "r").read()

    def run_whisper(self):
        transcript = openai.Audio.transcribe("whisper-1", self.audio_file)
        # Save the transcript to a file
        with open("transcript.txt", "w") as f:
            f.write(transcript.get("text"))
        return transcript
    
