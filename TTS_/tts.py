import os, pyttsx3, time


def text_to_speech(text):
    # Create a pyttsx3 object
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    
    # Set the properties for a more natural voice
    engine.setProperty('rate', 149)  # Adjust the speaking rate (words per minute)
    engine.setProperty('volume', 1)  # Increased speech volume
    engine.setProperty('pitch', 1.5)  # Use a neutral voice pitch
    engine.setProperty('intonation', 1.2)  # Slightly increased intonation
    engine.setProperty('wordgap', 10)
    # engine.setProperty('pitch', 150)



    # Convert text to speech
    paragraphs = text.split('\n\n')  # Split text into paragraphs
    for paragraph in paragraphs:
        # Add a pause before each paragraph
        time.sleep(0.8)

        # Convert each sentence within the paragraph
        sentences = paragraph.split('. ')
        for sentence in sentences:
            # Add a pause before each sentence
            time.sleep(0.2)

            commas = sentence.split(', ')
            for comma in commas:
                
                time.sleep(0.1)
                
                engine.say(comma)
            
        engine.runAndWait()
        
# from gtts import gTTS
# import playsound
# import os

# text = "Hello, how are you today?"

# tts = gTTS(text=text, lang='en', tld='co.uk')
# tts.save("output.mp3")

# playsound.playsound("output.mp3")

# os.remove("output.mp3")
