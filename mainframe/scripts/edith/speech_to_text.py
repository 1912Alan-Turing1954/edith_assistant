import torch
import pyaudio
import numpy as np
import time
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Path to the locally stored model and tokenizer
model_path = "./mainframe/scripts/data/database/models/wav2vec2-base-960h"
tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path).to(device)

# Define a simple noise gate threshold
NOISE_THRESHOLD = 550  # Adjust this threshold as needed
SILENCE_THRESHOLD = 2  # Silence duration in seconds to stop listening


def speech_to_text(audio):
    """Transcribe speech from audio input."""
    audio = audio.astype(np.float32)
    input_values = tokenizer(
        audio, return_tensors="pt", sampling_rate=16000
    ).input_values.to(device)
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription


def capture_audio(seconds=5):
    """Capture audio from microphone, focusing on direct noise."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Listening...")

    frames = []
    silence_timer = 0  # Timer to track silence duration
    listening = True  # Flag to control listening loop

    while listening:
        data = stream.read(CHUNK)
        audio_chunk = np.frombuffer(data, dtype=np.int16)

        # Check if audio chunk is above noise threshold
        if np.max(np.abs(audio_chunk)) > NOISE_THRESHOLD:
            frames.append(audio_chunk)
            silence_timer = 0  # Reset silence timer if speech is detected
        else:
            silence_timer += CHUNK / RATE  # Increment silence timer

        # Check for silence duration to stop listening
        if silence_timer > SILENCE_THRESHOLD:
            listening = False

    stream.stop_stream()
    stream.close()
    p.terminate()

    if frames:
        audio = np.concatenate(frames, axis=0)
        return audio
    else:
        return None
