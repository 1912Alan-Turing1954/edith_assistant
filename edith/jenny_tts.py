import os
import threading
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import simpleaudio as sa
from textblob import TextBlob

# Initialize ModelManager globally for caching
model_manager = ModelManager("TTS/TTS/.models.json")

# Global variables for model paths
MODEL_NAME = "tts_models/en/jenny/jenny"
SAVE_PATH = "Data/models/"
CHECKPOINT_PATH = os.path.join(SAVE_PATH, "model.pt")
CONFIG_PATH = os.path.join(SAVE_PATH, "config.json")

# Initialize or load the TTS model on script start
if os.path.exists(CHECKPOINT_PATH) and os.path.exists(CONFIG_PATH):
    # If the model files exist locally, load them
    print("Loading model locally: success")
else:
    # If the model files do not exist, download the model
    model_path, config_path, model_item = model_manager.download_model(MODEL_NAME)
    print("Downloading model: success")

    # Save the downloaded model to the local directory
    os.makedirs(SAVE_PATH, exist_ok=True)
    os.rename(model_path, CHECKPOINT_PATH)
    os.rename(config_path, CONFIG_PATH)

# Initialize the TTS synthesizer
syn = Synthesizer(
    tts_checkpoint=CHECKPOINT_PATH,
    tts_config_path=CONFIG_PATH,
    use_cuda=True,  # Adjust as needed
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


# import os
# import shutil
# import simpleaudio as sa
# from textblob import TextBlob
# from TTS.utils.manage import ModelManager
# from TTS.utils.synthesizer import Synthesizer

# # Initialize ModelManager globally for caching
# model_manager = ModelManager("TTS/TTS/.models.json")

# # Global variables for model paths
# MODEL_NAME = "tts_models/en/jenny/jenny"
# SAVE_PATH = "Data/models/"
# CHECKPOINT_PATH = os.path.join(SAVE_PATH, "model.pt")
# CONFIG_PATH = os.path.join(SAVE_PATH, "config.json")

# # Initialize or load the TTS model on script start
# if os.path.exists(CHECKPOINT_PATH) and os.path.exists(CONFIG_PATH):
#     # If the model files exist locally, load them
#     print("Loading model locally: success")
# else:
#     # If the model files do not exist, download the model
#     model_path, config_path, model_item = model_manager.download_model(MODEL_NAME)
#     print("Downloading model: success")

#     # Save the downloaded model to the local directory
#     os.makedirs(SAVE_PATH, exist_ok=True)
#     os.rename(model_path, CHECKPOINT_PATH)
#     os.rename(config_path, CONFIG_PATH)

# # Initialize the TTS synthesizer
# syn = Synthesizer(
#     tts_checkpoint=CHECKPOINT_PATH,
#     tts_config_path=CONFIG_PATH,
#     use_cuda=True,  # Adjust as needed
# )

# # Global variables to track the last two dialogue copies and sequence number
# last_dialogue_copies = []
# sequence_number = 1  # Start sequence number at 1


# def determine_emotion(text):
#     """
#     Determine the emotion of the text using TextBlob.
#     """
#     blob = TextBlob(text)
#     sentiment = blob.sentiment.polarity
#     if sentiment >= 0.6:
#         return "happy"
#     elif 0.3 <= sentiment < 0.6:
#         return "positive"
#     elif -0.2 < sentiment < 0.3:
#         return "neutral"
#     elif -0.6 <= sentiment < -0.2:
#         return "mad"
#     elif sentiment < -0.6:
#         return "sad"
#     else:
#         return "very_sad"


# def add_period_if_missing(text):
#     """
#     Add a period at the end of the text if it doesn't already have one.
#     """
#     if text.strip()[-1] not in [".", "!", "?"]:
#         return text.strip() + "."
#     else:
#         return text.strip()


# def generate_filename(sequence_number):
#     """
#     Generate a filename based on the sequence number.
#     """
#     return f"dialogue_{sequence_number}.wav"


# def text_to_speech(text, output_path=None):
#     """
#     Convert text to speech using the initialized TTS model.
#     """
#     global last_dialogue_copies, sequence_number

#     if text is None:
#         return None, None

#     # Add a period at the end of the text if missing
#     text = add_period_if_missing(text)

#     # Determine emotion of the text
#     emotion = determine_emotion(text)

#     # Perform text-to-speech synthesis
#     outputs = syn.tts(
#         text,
#         emotion=emotion,
#     )

#     # Save the synthesized audio to data/dialogue directory
#     dialogue_dir = "data/dialogue"
#     os.makedirs(dialogue_dir, exist_ok=True)

#     # Generate a new filename based on the current sequence number
#     output_filename = generate_filename(sequence_number)
#     output_path = os.path.join(dialogue_dir, output_filename)

#     # Increment the sequence number
#     sequence_number += 1

#     # Reset sequence number to 1 if it exceeds 2
#     # if sequence_number > 2:
#     # sequence_number = 1

#     syn.save_wav(outputs, output_path)

#     # Create a copy of the audio file before playing
#     copy_path = os.path.join(
#         dialogue_dir, f"{os.path.splitext(output_filename)[0]}_copy.wav"
#     )
#     shutil.copy(output_path, copy_path)

#     # Play the audio from the copied file
#     wave_obj = sa.WaveObject.from_wave_file(copy_path)
#     play_obj = wave_obj.play()

#     # Wait for playback to finish
#     play_obj.wait_done()

#     # Remove the original dialogue file after playing
#     if os.path.exists(output_path):
#         os.remove(output_path)

#     # Manage last_dialogue_copies list to keep track of the last 2 dialogue files
#     last_dialogue_copies.append(copy_path)
#     if len(last_dialogue_copies) > 2:
#         # Remove the oldest dialogue file copy
#         oldest_copy = last_dialogue_copies.pop(0)
#         if os.path.exists(oldest_copy):
#             os.remove(oldest_copy)

#     return play_obj, output_path
