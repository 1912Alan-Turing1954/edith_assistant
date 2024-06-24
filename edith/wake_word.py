import speech_recognition as sr
import time


class WakeWordDetector:
    def __init__(self, wake_word="friday"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def detect_wake_word(self):
        with self.microphone as source:
            print("Listening for wake word...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            wake_word_detected = self.recognizer.recognize_google(audio).lower()
            if self.wake_word in wake_word_detected:
                return True
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

        return False


class Assistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen_for_command(self):
        with self.microphone as source:
            print("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            user_input = self.recognizer.recognize_google(audio).lower()
            return user_input
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

        return None


# Example usage:
if __name__ == "__main__":
    wake_word_detector = WakeWordDetector()
    assistant = Assistant()

    while True:
        if wake_word_detector.detect_wake_word():
            print("Wake word detected!")
            print("Listening for command...")
            command = assistant.listen_for_command()

            if command:
                print(f"Command received: {command}")
                # Process the command here (implement your logic)
                break
            else:
                print("No command received. Waiting for response...")
                time.sleep(5)  # Wait for 5 seconds before checking again
                continue
