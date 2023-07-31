# import os, pyttsx3, time


# def text_to_speech(text):
#     # Create a pyttsx3 object
#     engine = pyttsx3.init()
    
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)
    
#     # Set the properties for a more natural voice
#     engine.setProperty('rate', 149)  # Adjust the speaking rate (words per minute)
#     engine.setProperty('volume', 1)  # Increased speech volume
#     engine.setProperty('pitch', 1.5)  # Use a neutral voice pitch
#     engine.setProperty('intonation', 1.2)  # Slightly increased intonation
#     engine.setProperty('wordgap', 10)
#     # engine.setProperty('pitch', 150)



#     # Convert text to speech
#     paragraphs = text.split('\n\n')  # Split text into paragraphs
#     for paragraph in paragraphs:
#         # Add a pause before each paragraph
#         time.sleep(0.8)

#         # Convert each sentence within the paragraph
#         sentences = paragraph.split('. ')
#         for sentence in sentences:
#             # Add a pause before each sentence
#             time.sleep(0.2)

#             commas = sentence.split(', ')
#             for comma in commas:
                
#                 time.sleep(0.1)
                
#                 engine.say(comma)
            
#         engine.runAndWait()

# from TTS.api import TTS



# Example usage:


from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

model_manager = ModelManager("C:/Users/1912a/Jarvis/.venv/Lib/site-packages/TTS/.models.json")

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

text = ""

outputs = syn.tts(text)
syn.save_wav(outputs, "audio-1.wav")