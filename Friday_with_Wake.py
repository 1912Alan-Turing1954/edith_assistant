import datetime
import speech_recognition as sr  # Import the speech_recognition library
from Friday_class import Friday

# Initialize the recognizer
recognizer = sr.Recognizer()

def is_wake_word(phrase):
    return "friday" in phrase.lower()

def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            phrase = recognizer.recognize_google(audio).lower()
            if is_wake_word(phrase):
                print("Wake word detected!")
                return
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Error occurred while requesting results from Google Speech Recognition service: {e}")

def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print(f"You said: {user_input}")
            # Rest of your code remains unchanged
            # ... (Your existing code from here) ...
        
            Friday.MainFrame(user_input)
                        
            # Once processing is done, break out of the listening loop
            break

        except sr.UnknownValueError:
            print("Sorry, I could not understand you.")
        except sr.RequestError as e:
            print(f"Error occurred while requesting results from Google Speech Recognition service: {e}")

# Main loop
while True:
    listen_for_wake_word()  # Wait for the wake word "friday" to activate listening
    while True:
        listen()  # Enter active listening mode and process user input
