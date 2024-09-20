import os
import threading
import sys
import sys

# sys.path.append(r"/home/hailwic/Repos/edith/scripts")

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
# from TTS.utils.manage import ModelManager
import simpleaudio as sa
from textblob import TextBlob


# Get the absolute path of the 'TTS' directory
model_manager = ModelManager('scripts/TTS/TTS/.models.json')

model_path, config_path, model_item = model_manager.download_model("tts_models/en/jenny/jenny")

# # Global variables for model paths
# MODEL_NAME = "tts_models/en/jenny/jenny"
# SAVE_PATH = "scripts/data/models/jenny_model/"
# CHECKPOINT_PATH = os.path.join(SAVE_PATH, "model.pt")
# CONFIG_PATH = os.path.join(SAVE_PATH, "config.json")

# print(CHECKPOINT_PATH)
# print(CONFIG_PATH)
# # Initialize or load the TTS model on script start
# if os.path.exists(CHECKPOINT_PATH) and os.path.exists(CONFIG_PATH):
#     # If the model files exist locally, load them
#     print("Loading jenny model: success")
# else:
#     # If the model files do not exist, download the model
#     model_path, config_path, model_item = model_manager.download_model(MODEL_NAME)
#     print("Downloading model: success")

#     # Save the downloaded model to the local directory
#     os.makedirs(SAVE_PATH, exist_ok=True)
#     os.rename(model_path, CHECKPOINT_PATH)
#     os.rename(config_path, CONFIG_PATH)

# Initialize the TTS synthesizer
syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    # use_cuda=True,  # Adjust as needed
    use_cuda=False,  # Adjust as needed

)


def determine_emotion(text):
    """
    Determine the emotion of the text using TextBlob.
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment >= 0.6:
        return "happy"
    elif 0.3 <= sentiment < 0.6:
        return "positive"
    elif -0.2 < sentiment < 0.3:
        return "neutral"
    elif -0.6 <= sentiment < -0.2:
        return "mad"
    elif sentiment < -0.6:
        return "sad"
    else:
        return "very_sad"


def add_period_if_missing(text):
    """
    Add a period at the end of the text if it doesn't already have one.
    """
    if text.strip()[-1] not in [".", "!", "?"]:
        return text.strip() + "."
    else:
        return text.strip()



def text_to_speech(text, output_path="audio.wav"):
    """
    Convert text to speech using the initialized TTS model.
    """
    if text is None:
        return

    # Add a period at the end of the text if missing
    text = add_period_if_missing(text)

    # Determine emotion of the text
    emotion = determine_emotion(text)

    # Perform text-to-speech synthesis
    outputs = syn.tts(
        text,
        emotion=emotion,

    )

  

    # Save the synthesized audio
    syn.save_wav(outputs, output_path)

    # Play the audio (optional)
    wave_obj = sa.WaveObject.from_wave_file(output_path)
    play_obj = wave_obj.play()
    # play_obj.wait_done()

    # Define a function to play the audio and clean up
    def play_audio():
        nonlocal play_obj
        play_obj.wait_done()

    # Create a thread to play audio
    thread = threading.Thread(target=play_audio)
    thread.start()

    # Return the thread object and temporary audio file path
    return thread, play_obj, output_path
    # # Delete the audio file after use (optional)
    # os.remove(output_path)



