from openai import OpenAI
import time
from pygame import mixer
import os
import sys
from dotenv import load_dotenv
import json
# import assistant_tools
import requests

load_dotenv()

# Get the OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client and mixer
client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key=openai_api_key)
mixer.init()
assistant_id = "<assistant_id>"
thread_id = "<thread_id>"

# Retrieve the assistant and thread
assistant = client.beta.assistants.retrieve(assistant_id)
thread = client.beta.threads.retrieve(thread_id)

# load api url
API_URL = os.getenv("API_URL")

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"