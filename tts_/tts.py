from TTS.api import TTS
import simpleaudio as sa
import os, re


def text_to_speech(text):
    # Initialize TTS with desired model
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)

    tts.tts_to_file(text, file_path="tts_/output.wav")

    # Run TTS
    filename = "tts_/output.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove("tts_/output.wav")


if __name__ == "__main__":
    # Example usage
    text = input("Enter text to convert to speech: ")
    text_to_speech(text)
