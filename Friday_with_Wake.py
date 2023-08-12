import datetime
import speech_recognition as sr  # Import the speech_recognition library
from Friday_class import Friday

friday = Friday()

# Initialize the recognizer
recognizer = sr.Recognizer()


def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=5, energy_threshold=300
            )

            try:
                phrase = recognizer.recognize_google(audio).lower()
                if phrase == "friday":
                    print("Wake word detected!")
                    return
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(
                    f"Error occurred while requesting results from Google Speech Recognition service: {e}"
                )


def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=5, energy_threshold=300
            )

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print(f"You said: {user_input}")
            # Rest of your code remains unchanged
            # ... (Your existing code from here) ...

            friday.MainFrame(user_input)

            # Once processing is done, break out of the listening loop
            break

        except sr.UnknownValueError:
            print("Sorry, I could not understand you.")
        except sr.RequestError as e:
            print(
                f"Error occurred while requesting results from Google Speech Recognition service: {e}"
            )


# Main loop
while True:
    #     # listen_for_wake_word()  # Wait for the wake word "friday" to activate listening
    #     # while True:
    listen()  # Enter active listening mode and process user input
