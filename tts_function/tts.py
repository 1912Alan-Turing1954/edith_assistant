from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import os
import simpleaudio as sa


def text_to_speech(
    text, model_name="tts_models/en/jenny/jenny", output_path="audio.wav"
):
    # Initialize the model manager
    path = "TTS/TTS/.models.json"
    model_manager = ModelManager(path)

    # Download the TTS model
    model_path, config_path, model_item = model_manager.download_model(model_name)

    # Initialize Synthesizer with GPU usage
    syn = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        use_cuda=True,  # Specify GPU usage
    )

    # Perform text-to-speech synthesis
    outputs = syn.tts(text)

    # Save the synthesized audio
    syn.save_wav(outputs, output_path)

    # Play the audio
    wave_obj = sa.WaveObject.from_wave_file(output_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # Delete the audio file after use
    os.remove(output_path)


# Example usage:
text_to_speech("Hello from a machine")
