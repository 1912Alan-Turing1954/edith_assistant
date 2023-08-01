from coqui.TTS.api import TTS
import simpleaudio as sa
import os

def text_to_speech(text):
    
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=False)
    tts.tts_to_file(text, file_path='tts_/output.wav')
    
    # Run TTS
    filename = 'tts_/output.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove('tts_/output.wav') 

