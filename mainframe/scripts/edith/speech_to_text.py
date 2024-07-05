import torch
import pyaudio
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Path to the locally stored model and tokenizer
model_path = "./mainframe/scripts/data/database/models/wav2vec2-base-960h"
tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path).to(device)

# Define a simple noise gate threshold
NOISE_THRESHOLD = 550  # Adjust this threshold as needed


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
    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        audio_chunk = np.frombuffer(data, dtype=np.int16)

        # Apply noise gate
        if np.max(np.abs(audio_chunk)) > NOISE_THRESHOLD:
            frames.append(audio_chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if frames:
        audio = np.concatenate(frames, axis=0)
        return audio
    else:
        return None
