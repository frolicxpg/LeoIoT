# LeoIoT: Raspberry Pi Zero 2W Home Assistant

LeoIoT is a Python-based home assistant designed to run on Raspberry Pi Zero 2W as a local voice interface for smart home control. This project connects to a cloud AI server (Raspberry Pi 5) for advanced speech recognition and AI-powered responses.

## Overview

- **Local Device:** Raspberry Pi Zero 2W with ReSpeaker 2-Mic Pi Hat and speaker
- **Cloud Server:** Raspberry Pi 5 (runs Flask API, Vosk, OpenAI GPT, TTS, etc.)
- **Role:** Pi Zero 2W handles wake word detection, records voice, sends audio to the cloud, and plays AI responses.

## Hardware Setup (Pi Zero 2W)

- **Audio Input:** ReSpeaker 2-Mic Pi Hat on GPIO
- **Audio Output:** Small speaker via PAM8403 amp module (wired with soldering and jumper wires)
- **Power:** Single USB Type-C powers both Pi Zero and amp module in parallel
- **Noise Solution:** Ground loop isolator added between ReSpeaker aux out and amp module in to eliminate buzzing

## Software Flow

1. **Wake Word Detection:** Vosk mini-model listens for wake-word using Pi Zero 2W.
2. **Voice Recording:** Starts recording on wake word; stops when user finishes speaking (audio stream logic).
3. **Audio Streaming:** Sends audio to cloud server (Raspberry Pi 5) via API.
4. **Response Playback:** Receives AI-generated speech from cloud and plays via speaker.

## Getting Started

### Prerequisites

- Raspberry Pi Zero 2W
- ReSpeaker 2-Mic Pi Hat
- PAM8403 amp module, speaker, jumper wires, soldering tools

### Installation

```bash
git clone https://github.com/frolicxpg/LeoIoT.git
cd LeoIoT/
pip install -r requirements.txt
python main.py
```

- Configure API endpoint for your cloud server in config files.

## Troubleshooting

- **Buzzing Noise:** Use a ground loop isolator between ReSpeaker output and amp module input.
- **Wake Word Accuracy:** Add multiple similar-sounding words to model for better detection.

## Contact

Created by [frolicxpg](https://github.com/frolicxpg). Open an issue for support or collaboration.
