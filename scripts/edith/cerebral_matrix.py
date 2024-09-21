import threading
import datetime
import logging
import os
import random
import re
import torch
import json
from tqdm import tqdm
import time
import enchant
import warnings
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from modules.jenny_tts import text_to_speech
from modules.system_info import *
from modules.network_tools import *
from large_language_model.llm_main import handle_conversation

# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')


class EdithMainframe:
    def __init__(self, intents_file: str, data_file: str):
        self.intents_file = intents_file
        self.data_file = data_file
        self.load_intents_and_model()

        # Initialize instance variables
        self.prev_tag = ""
        self.prev_response = ""
        self.stop_response = ""
        self.play_obj = None
        self.output_path = None
        self.stopped = False
        self.response = None
        self.is_in_conversation = False
        self.conversation_timeout = 90
        self.last_interaction_time = datetime.datetime.now()
        self.load_settings()

    def load_intents_and_model(self) -> None:
        """Load intents and model from files."""
        with open(self.intents_file, "r") as json_data:
            self.intents = json.load(json_data)

        data = torch.load(self.data_file, weights_only=True)
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def classify_intent(self, user_input: str) -> tuple:
        """Classify user input to determine intent."""
        sentence = tokenize(user_input.lower())
        X = bag_of_words(sentence, self.all_words).reshape(1, -1)
        X = torch.from_numpy(X)
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]
        prob = torch.softmax(output, dim=1)[0][predicted.item()].item()
        return tag, prob

    def convert_decimal_to_verbal(self, sentence: str) -> str:
        """Convert decimal numbers in a sentence to verbal form."""
        return re.sub(r'\b\d+\.\d+\b', self._replace_decimal, sentence)

    def _replace_decimal(self, match) -> str:
        """Helper method to replace decimal match with verbal representation."""
        number = match.group(0)
        integer_part, decimal_part = number.split('.')
        return f"{integer_part} point {decimal_part}"

    def get_updated_system_info(self):
        """Get updated system information."""
        return get_system_info()

    def replace_symbols(self, expression: str) -> str:
        """Replace mathematical symbols in an expression with descriptive phrases."""
        symbol_map = {
            '/': ' divided by ',
            '+': ' plus ',
            '-': ' minus ',
            '*': ' multiplied by ',
            '^': ' raised to the power of ',
            '=': ' equals '
        }
        for symbol, description in symbol_map.items():
            expression = expression.replace(symbol, description)
        return expression

    def get_intent_response(self, intent, response: str, replacement: str = None) -> None:
        """Get the response for an intent, with optional replacement."""
        if replacement:
            response = response.replace("{string}", replacement)
        self.prev_tag = intent["tag"]
        self.prev_response = response
        self.response = response

    def stop_audio(self) -> None:
        """Stop current audio playback and remove the output file if exists."""
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            if self.output_path and os.path.exists(self.output_path):
                os.remove(self.output_path)

    def clean_input(self, user_input: str) -> str:
        """Clean the user input by converting decimal points and removing commas."""
        cleaned_input = re.sub(r"(\d+)\.(\d+)", r"\1 point \2", user_input)
        return re.sub(r'(?<=\d),(?=\d)', '', cleaned_input)

    def detect_wake_word(self, transcription: str) -> bool:
        """Detect if the wake word 'edith' is present in the transcription."""
        return "edith" in transcription.lower()

    def clean_text(self, text: str) -> str:
        """Clean text by correcting misspelled words."""
        d = enchant.Dict("en_US")
        words = text.split()
        cleaned_words = [word if d.check(word) else d.suggest(word)[0] for word in words if d.suggest(word)]
        return " ".join(cleaned_words)    

    def load_settings(self) -> None:
        """Loads settings from a JSON file if it exists."""
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    
                self.conversation_timeout = settings.get('conversation_timeout', self.conversation_timeout)
                self.intents_file = settings.get('intents_file', self.intents_file)
                self.data_file = settings.get('data_file', self.data_file)

                # Set logging level
                logging_level = settings.get('logging_level', logging.getLevelName(logging.root.level))
                logging.getLogger().setLevel(logging.getLevelName(logging_level))

                print(" ➤ Settings loaded successfully from 'settings.json'.")
            except Exception as e:
                print(f" ❌ Failed to load settings: {e}")

    def save_settings(self) -> None:
        """Saves the current settings to a JSON file."""
        settings = {
            'conversation_timeout': self.conversation_timeout,
            'intents_file': self.intents_file,
            'data_file': self.data_file,
            'logging_level': logging.getLevelName(logging.root.level),
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            print(" ➤ Settings saved successfully to 'settings.json'.")
        except Exception as e:
            print(f" ❌ Failed to save settings: {e}")


    def settings_menu(self) -> None:
        """Display a sci-fi inspired BIOS settings menu with effects."""
        while True:
            print("\n" + "=" * 70)
            print("           ██████████ BIOS Settings Interface ██████████")
            print("=" * 70)
            print(" [1] Change Conversation Timeout (Current: {}s)".format(self.conversation_timeout))
            print(" [2] Change Intents File Path (Current: {})".format(self.intents_file))
            print(" [3] Change Data File Path (Current: {})".format(self.data_file))
            print(" [4] Change Logging Level (Current: {})".format(logging.getLevelName(logging.root.level)))
            print(" [5] Save current settings to file")
            print(" [6] Exit Settings")
            print("=" * 70)

            choice = input(" Select an option [1-5]: ")

            if choice == "1":
                new_timeout = input(" Enter new conversation timeout in seconds: ")
                try:
                    self.conversation_timeout = int(new_timeout)
                    print(" ➤ Updating conversation timeout...", end='')
                    for _ in tqdm(range(10), desc='Processing', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
                        time.sleep(0.1)  # Simulate processing time
                    print(" Updated to {} seconds.".format(self.conversation_timeout))
                except ValueError:
                    print(" ❌ Invalid input. Please enter a valid integer.")
            elif choice == "2":
                new_intents_file = input(" Enter new intents file path: ")
                self.intents_file = new_intents_file
                print(" ➤ Updating intents file path...", end='')
                for _ in tqdm(range(10), desc='Processing', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
                    time.sleep(0.1)  # Simulate processing time
                print(" Updated.")
            elif choice == "3":
                new_data_file = input(" Enter new data file path: ")
                self.data_file = new_data_file
                print(" ➤ Updating data file path...", end='')
                for _ in tqdm(range(10), desc='Processing', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
                    time.sleep(0.1)  # Simulate processing time
                print(" Updated.")
            elif choice == "4":
                new_logging_level = input(" Enter new logging level (DEBUG, INFO, WARNING, ERROR): ").upper()
                levels = {
                    'DEBUG': logging.DEBUG,
                    'INFO': logging.INFO,
                    'WARNING': logging.WARNING,
                    'ERROR': logging.ERROR
                }
                if new_logging_level in levels:
                    logging.getLogger().setLevel(levels[new_logging_level])
                    print(" ➤ Updating logging level...", end='')
                    for _ in tqdm(range(10), desc='Processing', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
                        time.sleep(0.1)  # Simulate processing time
                    print(" Updated to {}.".format(new_logging_level))
                else:
                    print(" ❌ Invalid logging level.")
            elif choice == "5":
                print(" ➤ Saving current settings...", end='')
                self.save_settings()  # Call the save method
            elif choice == "6":
                print(" Exiting settings menu.")
                break
            else:
                print(" ❌ Invalid choice. Please select a valid option.")


    def operational_matrix(self) -> None:
        """Main loop for handling user input and generating responses."""
        while True:
            try:
                transcription = self.get_user_input()

                if transcription == "access bios":
                    self.settings_menu()
                    continue

                if self.detect_wake_word(transcription):
                    self.start_conversation()
                
                if self.is_in_conversation and self.is_within_timeout():
                    transcription = self.prepare_transcription(transcription)
                    tag, prob = self.classify_intent(transcription)

                    if prob > 0.9999:
                        self.handle_intent_response(tag, transcription)
                    else:
                        self.handle_low_confidence(transcription)
                else:
                    self.is_in_conversation = False

            except Exception as e:
                logging.error("An error occurred: %s", e)

    def get_user_input(self) -> str:
        """Get and clean user input."""
        transcription = input("Enter transcript:").lower().strip()
        return self.clean_text(transcription)

    def start_conversation(self) -> None:
        """Initialize conversation state."""
        logging.info("Wake word detected...")
        self.is_in_conversation = True
        self.last_interaction_time = datetime.datetime.now()

    def is_within_timeout(self) -> bool:
        """Check if the conversation is still within timeout."""
        return (datetime.datetime.now() - self.last_interaction_time).total_seconds() < self.conversation_timeout

    def prepare_transcription(self, transcription: str) -> str:
        """Prepare transcription by removing the wake word."""
        return transcription.replace("edith", "") if transcription.lower() != "edith" else 'edith'

    def handle_low_confidence(self, transcription: str) -> None:
        """Handle the case when intent classification confidence is low."""
        logging.info("Confidence below threshold. Using LLM.")
        self.response = None
        self.stop_audio()
        response = handle_conversation(transcription)
        response = self.convert_decimal_to_verbal(response)
        self.thread, self.play_obj, self.output_path = text_to_speech(response)

    def handle_intent_response(self, tag: str, user_input: str) -> None:
        """Handle the intent based on the tag and generate the appropriate response."""
        responses = {
            "storage_info_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                generate_storage_status_response()
            ),
            "cpu_usage_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                generate_cpu_usage_response()
            ),
            "memory_usage_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                generate_memory_usage_response()
            ),
            "disk_space_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                generate_disk_space_response()
            ),
            "ping_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                network_function(user_input)
            ),
            "speedtest_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                download_speed_test()
            ),
            "check_internet_tsk": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                check_internet()
            ),
            "system_status": lambda: self.get_intent_response(
                self.intents["intents"][tag],
                random.choice(self.intents["intents"][tag]["responses"]),
                get_live_system_status_response()
            ),
        }
        
        if tag in responses:
            responses[tag]()
        else:
            self.get_intent_response(self.intents["intents"][tag], random.choice(self.intents["intents"][tag]["responses"]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    intents_model = EdithMainframe("edith/data/intents.json", "edith/data/data.pth")
# 
    while True:
        try:
            intents_model.operational_matrix()
        except Exception as e:
            logging.error("An error occurred in the main loop: %s", e)
