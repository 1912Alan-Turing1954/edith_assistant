from TTS.api import TTS
import simpleaudio as sa
import os, re


def text_to_speech(text):
    decimal_pattern = r"\d+\.\d+"

    # Find all occurrences of the pattern in the text
    decimal_matches = re.findall(decimal_pattern, text)

    # Replace decimal points with "point"
    for match in decimal_matches:
        text = text.replace(
            match, match.replace(".", " point "), 1
        )  # Replace only the first occurrence

    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)
    tts.tts_to_file(text, file_path="tts_/output.wav")

    # Run TTS
    filename = "tts_/output.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove("tts_/output.wav")
