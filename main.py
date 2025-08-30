import sounddevice as sd
import queue
import sys
import json
import time
import requests
from vosk import Model, KaldiRecognizer
import assist  # Your TTS module
from pygame import mixer

# Load models
ENGLISH_MODEL = Model("vosk-model-small-en-us-0.15")
HINDI_MODEL = Model("vosk-model-hi-0.22")
sample_rate = 16000
q = queue.Queue()

wake_words = ["leo", "hello"] # Add your wake words here e.g., ["leo", "hello"]

# Callback for mic input
def callback(indata, status):
    if status:
        print("Audio input status:", status, file=sys.stderr)
    q.put(bytes(indata))
    
# Start input stream
stream = sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback)

print("Wake word listener started...")

while True:
    stream.start()
    recognizer = KaldiRecognizer(ENGLISH_MODEL, sample_rate)

    wake_detected = False

    print("Listening for wake word...")

    while not wake_detected:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            text = json.loads(recognizer.Result()).get("text", "")
            print("Heard:", text)
            for word in wake_words:
                if word in text.lower():
                    print(f"🔊 Wake word '{word}' detected!")
                    wake_detected = True
                    # wake.wav audio file playback
                    mixer.init()
                    mixer.music.load("wake.wav")
                    mixer.music.play()
                    break

    stream.stop()
    time.sleep(0.1)

    # After wake word is heard, listen to user input
    print("🎤 Listening for command...")
    stream.start()
    audio_sample = b""
    speech_recognizer = KaldiRecognizer(ENGLISH_MODEL, sample_rate)

    while True:
        data = q.get()
        audio_sample += data
        if speech_recognizer.AcceptWaveform(data):
            break

    stream.stop()

    print("Captured speech. Processing...")

    response = requests.post(
        "http://10.147.17.1:5555/recognize",
        data=audio_sample,
        headers={"Content-Type": "application/octet-stream"}
    )

    if response.ok:
        recognized_text = response.json().get("text")
        print("Server recognized:", recognized_text)
    else:
        print("❌ Error from recognition server:", response.text)
        continue

    # Send to API and speak
    try:
        api_url = "http://10.147.17.1:5555/process"
        payload = {"input": recognized_text}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        reply = response.json().get("response", "")
        if not reply:
            print("❌ No response from API.")
            continue

        print("🤖 Lino:", reply)
        assist.TTS(reply)

    except Exception as e:
        print("❌ API or TTS error:", e)

    print("\nReturning to wake word detection...")
