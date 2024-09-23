import torch
import pyaudio
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model and tokenizer
model_path = "scripts/data/models/wav2vec2-base-960h"
tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path).to(device)

# Define constants
# Define constants with lower thresholds
NOISE_THRESHOLD = 300  # Adjust this threshold as needed (lower value)
SILENCE_THRESHOLD = 1.5  # Silence duration in seconds to stop listening (lower value)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def speech_to_text(audio):
    """Transcribe speech from audio input."""
    audio = audio.astype(np.float32)
    input_values = tokenizer(audio, return_tensors="pt", sampling_rate=RATE).input_values.to(device)
    
    with torch.no_grad():
        logits = model(input_values).logits
    
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription

def capture_audio():
    """Capture audio from the microphone, focusing on direct noise."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening...")
    frames = []
    silence_timer = 0

    while True:
        data = stream.read(CHUNK)
        audio_chunk = np.frombuffer(data, dtype=np.int16)

        if np.max(np.abs(audio_chunk)) > NOISE_THRESHOLD:
            frames.append(audio_chunk)
            silence_timer = 0  # Reset silence timer
        else:
            silence_timer += CHUNK / RATE  # Increment silence timer

        # Stop listening if silence exceeds threshold
        if silence_timer > SILENCE_THRESHOLD:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.concatenate(frames, axis=0) if frames else None

if __name__ == "__main__":
    while True:
        audio = capture_audio()
        if audio is not None:
            transcription = speech_to_text(audio)
            print(transcription)
        else:
            print("No audio captured.")
