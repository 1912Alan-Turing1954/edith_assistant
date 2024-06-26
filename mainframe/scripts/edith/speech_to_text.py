import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Path to the directory containing locally stored model and tokenizer
model_path = "./data/database/models/wav2vec2-base-960h"

# Load pre-trained model and tokenizer from local directory
tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path)


def speech_to_text(audio):
    # Load audio file
    speech, rate = librosa.load(audio, sr=16000)

    # Tokenize the speech input
    input_values = tokenizer(speech, return_tensors="pt").input_values

    # Store logits (non-normalized predictions)
    logits = model(input_values).logits

    # Store predicted id's
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the audio to generate text
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription
