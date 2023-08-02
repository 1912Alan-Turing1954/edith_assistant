from TTS.api import TTS
import simpleaudio as sa
import os

def text_to_speech(text):
    
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)
    tts.tts_to_file(text, file_path='tts_/output.wav', speed=0.8)
    
    # Run TTS
    filename = 'tts_/output.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove('tts_/output.wav') 
