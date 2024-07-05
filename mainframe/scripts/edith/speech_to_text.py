import torch
import pyaudio
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Path to the directory containing locally stored model and tokenizer
model_path = "./mainframe/scripts/data/database/models/wav2vec2-base-960h"
tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path)


# Function to transcribe speech from audio input
def speech_to_text(audio):
    # Ensure audio is in float32
    audio = audio.astype(np.float32)
    # Tokenize the speech input
    input_values = tokenizer(
        audio, return_tensors="pt", sampling_rate=16000
    ).input_values
    # Store logits (non-normalized predictions)
    logits = model(input_values).logits
    # Store predicted id's
    predicted_ids = torch.argmax(logits, dim=-1)
    # Decode the audio to generate text
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription


# Function to capture audio from microphone
def capture_audio(seconds=5):
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
        frames.append(np.frombuffer(data, dtype=np.int16))

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio = np.concatenate(frames, axis=0)

    return audio
