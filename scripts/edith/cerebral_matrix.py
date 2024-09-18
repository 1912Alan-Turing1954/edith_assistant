
# import datetime
# import glob
# import logging
# import os
# import pickle
# import random
# import re
# import shutil
# import torch
# import json
# import enchant
# import warnings
# warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# # from speech_to_text import *

# from brain.model import NeuralNet
# from brain.nltk_utils import bag_of_words, tokenize
# from modules.jenny_tts import text_to_speech  # Assuming this import is correct
# from modules.system_info import *  # Adjusted import to specific function
# from modules.network_tools import *
# # from speech_to_text import *
# import enchant
# # from mainframe.scripts.data.database.large_language_model.llm_ import llm
# from data.database.large_language_model.llm_ import *

# import sqlite3
# import os
# import datetime

# class DialogueManager:
#     def __init__(self, dialogue_archive, backup_dir):
#         self.dialogue_archive = dialogue_archive
#         self.backup_dir = backup_dir
#         self._initialize_database()

#     def _initialize_database(self):
#         # Create SQLite database if not exists
#         self.conn = sqlite3.connect(self.dialogue_archive)
#         self.cursor = self.conn.cursor()

#         # Create dialogue table if not exists
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS dialogue (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_input TEXT,
#                 bot_response TEXT,
#                 timestamp TEXT
#             )
#         ''')
#         self.conn.commit()

#     def save_dialogue_archive(self, user_input, bot_response):
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         # Insert new dialogue entry into the database
#         self.cursor.execute('''
#             INSERT INTO dialogue (user_input, bot_response, timestamp)
#             VALUES (?, ?, ?)
#         ''', (user_input, bot_response, timestamp))
#         self.conn.commit()

#     def backup_dialogue_archive(self):
#         # Ensure backup directory exists
#         os.makedirs(self.backup_dir, exist_ok=True)

#         # Generate new backup file name
#         backup_file = os.path.join(
#             self.backup_dir,
#             f"dialogue_archive_backup_.db",
#         )

#         # Copy current dialogue archive file to backup
#         shutil.copyfile(self.dialogue_archive, backup_file)
#         print(f"Backup created: {backup_file}")


# class Edith_Mainframe(object):
#     def __init__(self, intents_file, data_file):
#         self.intents_file = intents_file
#         self.data_file = data_file
#         self.load_intents_and_model()

#         self.prev_tag = ""
#         self.prev_response = ""
#         self.stop_response = ""

#         self.play_obj = None
#         self.output_path = None
#         self.stopped = False
#         self.response = None
#         self.dialogue_archive = "mainframe/scripts/data/database/archives/dialogue/dialogue_archives.bin"
#         self.backup_dir = "mainframe/scripts/data/database/archives/dialogue"

#         self.is_in_conversation = False  # Flag to track if in conversation
#         self.conversation_timeout = 60  # Timeout in seconds for conversation reset
#         self.last_interaction_time = datetime.datetime.now()
#         self.dialogue_manager = DialogueManager('mainframe/scripts/data/database/archives/dialogue/dialogue_archive.db', 'backup_dir')


#     def load_intents_and_model(self):
#         with open(self.intents_file, "r") as json_data:
#             self.intents = json.load(json_data)

#         data = torch.load(self.data_file)
#         self.all_words = data["all_words"]
#         self.tags = data["tags"]
#         input_size = data["input_size"]
#         hidden_size = data["hidden_size"]
#         output_size = data["output_size"]
#         model_state = data["model_state"]

#         self.model = NeuralNet(input_size, hidden_size, output_size)
#         self.model.load_state_dict(model_state)
#         self.model.eval()



#     def classify_intent(self, user_input):
#         sentence = tokenize(user_input.lower())
#         X = bag_of_words(sentence, self.all_words)
#         X = X.reshape(1, X.shape[0])
#         X = torch.from_numpy(X)
#         output = self.model(X)
#         _, predicted = torch.max(output, dim=1)
#         tag = self.tags[predicted.item()]
#         probs = torch.softmax(output, dim=1)
#         prob = probs[0][predicted.item()]
#         return tag, prob.item()

#     def get_time(self):
#         time_ = datetime.datetime.now().time().strftime("%I:%M %p")
#         if "PM" in time_:
#             time_ = time_.replace("PM", "P M")
#         elif "AM" in time_:
#             time_ = time_.replace("AM", "A M")
#         return time_

#     def get_date(self):
#         date_ = datetime.datetime.now().date().strftime("%B %d, %Y")
#         return date_

#     def get_day(self):
#         day_ = datetime.datetime.now().strftime("%A")
#         return day_

#     def convert_decimal_to_verbal(self, sentence):
#     # Define a function to convert each decimal number
#         def replace_decimal(match):
#             number = match.group(0)
#             # Split the number into integer and decimal parts
#             integer_part, decimal_part = number.split('.')
#             # Construct the verbal representation
#             return f"{integer_part} point {decimal_part}"

#         # Use a regular expression to find all decimal numbers in the sentence
#         return re.sub(r'\b\d+\.\d+\b', replace_decimal, sentence)

#     def get_updated_system_info(self):
#         return get_system_info()
    
#     def replace_symbols(self, expression):
#         # Define a mapping of symbols to their descriptions
#         symbol_map = {
#             '/': ' divided by ',
#             '+': ' plus ',
#             '-': ' minus ',
#             '*': ' multiplied by ',
#             '^': ' raised to the power of ',
#             '=': ' equals ',
#             # Add more symbols and their descriptions as needed
#         }
        
#         # Replace each symbol in the expression with its descriptive phrase
#         for symbol, description in symbol_map.items():
#             expression = expression.replace(symbol, description)
        
#         return expression



#     def get_intent_response(self, intent, response, replacement=None):
#         if replacement:
#             response = response.replace("{string}", replacement)

#         self.prev_tag = intent["tag"]
#         self.prev_response = response
#         self.response = response

#     def stop_audio(self):
#         # Stop current audio playback
#         if self.play_obj and self.play_obj.is_playing():
#             self.play_obj.stop()
#             if self.output_path and os.path.exists(self.output_path):
#                 os.remove(self.output_path)

#     def stopping(self):
#         # Stop current audio playback
#         if self.play_obj and self.play_obj.is_playing():
#             self.stop_response = self.prev_response
#             self.play_obj.stop()
#             self.stopped = True
#             if self.output_path and os.path.exists(self.output_path):
#                 os.remove(self.output_path)
#             return self.stop_response
#         else:
#             self.stopped = False

#     def clean_input(self, user_input):
#         pattern = r"(\d+)\.(\d+)"
#         cleaned_input = re.sub(pattern, r"\1 point \2", user_input)
#         cleaned_input = re.sub(r'(?<=\d),(?=\d)', '', cleaned_input)
#         return cleaned_input

#     def detect_wake_word(self, transcription):
#         return "edith" in transcription.lower()

#     def clean_text(self, text):
#         d = enchant.Dict("en_US")
#         words = text.split()
#         cleaned_words = []

#         for word in words:
#             if d.check(word):
#                 cleaned_words.append(word)
#             else:
#                 suggestions = d.suggest(word)
#                 if suggestions:
#                     cleaned_words.append(suggestions[0])
#         cleaned_text = " ".join(cleaned_words)
#         return cleaned_text

#     def Operational_Matrix(self):
#         while True:
#             try:
#                 # audio = capture_audio()
#                 # transcription = speech_to_text(
#                 #     audio
#                 # )  # Replace with your speech to text function

#                 transcription = input("Enter transcript:")

#                 transcription = self.clean_text(transcription.lower().strip())

#                 print("User input:", transcription)



#                 if self.detect_wake_word(transcription):
#                     print("Edith Detected")
#                     self.is_in_conversation = True
#                     self.last_interaction_time = datetime.datetime.now()

#                 # Check if still within conversation timeout
#                 if (
#                     self.is_in_conversation
#                     and (
#                         datetime.datetime.now() - self.last_interaction_time
#                     ).total_seconds()
#                     < self.conversation_timeout
#                 ):
#                     if transcription.lower() == "edith":
#                         self.stopping()
#                         transcription = 'edith'
#                     else:
#                         transcription = transcription.lower().replace("edith", "")



#                     tag, prob = self.classify_intent(transcription)

#                     print("User input:", transcription)

#                     print(prob)
#                     # Adjust the confidence threshold as needed
#                     if prob > 0.9999:
#                         intent_found = False
#                         for intent in self.intents["intents"]:
#                             if tag == intent["tag"]:
#                                 print("Intent matched:", tag)
#                                 intent_found = True
#                                 self.handle_intent(intent, transcription)
#                                 break  # Exit loop once intent is found
#                         if not intent_found:
#                             self.response = None
#                     else:
#                         self.response = None
#                         print("Confidence below threshold. Using LLM.")


#                     if self.response:
#                         self.stop_audio()
#                         self.response = self.convert_decimal_to_verbal(self.response)
#                         self.response = re.sub(r'(?<=\d),(?=\d)', '', self.response)
#                         self.response = self.replace_symbols(self.response)
#                         self.thread, self.play_obj, self.output_path = text_to_speech(self.response)

#                     else:
#                         self.stop_audio()
#                         response = llm_main(transcription)
#                         response = re.sub(r'(?<=\d),(?=\d)', '', response)
#                         response = self.convert_decimal_to_verbal(response)
#                         response = self.replace_symbols(response)
#                         self.thread, self.play_obj, self.output_path = text_to_speech(
#                             response
#                         )

#                     if self.response is None:
#                         self.dialogue_manager.save_dialogue_archive(transcription, response)
#                         self.dialogue_manager.backup_dialogue_archive()
#                     else:
#                         self.dialogue_manager.save_dialogue_archive(transcription, self.response)
#                         self.dialogue_manager.backup_dialogue_archive()
#                 else:
#                     self.is_in_conversation = False

#             except Exception as e:
#                 logging.error("An error occurred: %s", e)

#     def handle_intent(self, intent, user_input=None):
#         if intent["tag"] == "repeat_tsk" and self.stopped:
#             if self.prev_tag == "repeat_tsk":
#                 self.get_intent_response(intent, f"{self.stop_response}")
#             else:
#                 self.get_intent_response(intent, f"{random.choice(intent['responses'])} {self.stop_response}")
#             self.stop_response = ""
#             self.stopped = False
#         elif intent["tag"] == "repeat_tsk":
#             if self.prev_tag == "repeat_tsk":
#                 print("previous tag is repeat_tsk")
#                 self.get_intent_response(intent, f"{self.prev_response}")
#             else:
#                 print("previous tag is repeat_tsk")
#                 self.get_intent_response(intent, f"{random.choice(intent['responses'])} {self.prev_response}")
#         elif intent["tag"] == "system_info_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]), self.get_updated_system_info())
#         elif intent["tag"] == "storage_info_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]), generate_storage_status_response(get_system_info()))
#         elif intent["tag"] == "cpu_usage_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]), generate_cpu_usage_response(get_system_info()))
#         elif intent["tag"] == "memory_usage_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]), generate_memory_usage_response(get_system_info()))
#         elif intent["tag"] == "disk_space_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]), generate_disk_space_response(get_system_info()))
#         elif intent["tag"] == "time_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{time}", self.get_time()))
#         elif intent["tag"] == "date_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{date}", self.get_date()))
#         elif intent["tag"] == "day_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{day}", self.get_day()))
#         elif intent["tag"] == "ping_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", network_function(user_input)))
#         elif intent["tag"] == "speedtest_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", download_speed_test()))
#         elif intent["tag"] == "check_internet_tsk":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", check_internet()))
#         elif intent["tag"] == "system_status":
#             self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", get_live_system_status_response()))
#         else:
#             self.get_intent_response(intent, random.choice(intent["responses"]))


# if __name__ == "__main__":
#     intents_model = Edith_Mainframe("mainframe/scripts/edith/data/intents.json",
#                                     "mainframe/scripts/edith/data/data.pth")

#     while True:
#         try:
#             intents_model.Operational_Matrix()

#         except Exception as e:
#             logging.error("An error occurred in main loop: %s", e)


import datetime
import glob
import logging
import os
import pickle
import random
import re
import shutil
import torch
import json
import enchant
import sqlite3
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Import modules
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from modules.jenny_tts import text_to_speech
from modules.system_info import *  # Adjusted import to specific functions
from modules.network_tools import *
from large_language_model.llm_main import handle_conversation  # Assuming llm_main function exists
class DialogueManager:
    def __init__(self, dialogue_archive, backup_dir):
        self.dialogue_archive = dialogue_archive
        self.backup_dir = backup_dir
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the SQLite database."""
        self.conn = sqlite3.connect(self.dialogue_archive)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialogue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                AI_response TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def save_dialogue_archive(self, user_input, bot_response):
        """Save a dialogue entry to the database."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO dialogue (user_input, AI_response, timestamp)
            VALUES (?, ?, ?)
        ''', (user_input, bot_response, timestamp))
        self.conn.commit()

    def backup_dialogue_archive(self):
        """Backup the dialogue archive to a backup directory."""
        os.makedirs(self.backup_dir, exist_ok=True)
        backup_file = os.path.join(self.backup_dir, "dialogue_archive_backup_.db")
        shutil.copyfile(self.dialogue_archive, backup_file)
        print(f"Backup created: {backup_file}")

class Edith_Mainframe:
    def __init__(self, intents_file, data_file):
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
        self.dialogue_archive = "scripts/data/archives/dialogue/dialogue_archives.bin"
        self.backup_dir = "scripts/data/archives/dialogue"
        self.is_in_conversation = False
        self.conversation_timeout = 60
        self.last_interaction_time = datetime.datetime.now()
        self.dialogue_manager = DialogueManager(
            'scripts/data/archives/dialogue/dialogue_archive.db', 
            'backup_dir'
        )

    def load_intents_and_model(self):
        """Load intents and model from files."""
        with open(self.intents_file, "r") as json_data:
            self.intents = json.load(json_data)

        data = torch.load(self.data_file)
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def classify_intent(self, user_input):
        """Classify user input to determine intent."""
        sentence = tokenize(user_input.lower())
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        return tag, prob.item()

    def get_time(self):
        """Get current time in a specific format."""
        time_ = datetime.datetime.now().time().strftime("%I:%M %p")
        return time_.replace("PM", "P M").replace("AM", "A M")

    def get_date(self):
        """Get current date in a specific format."""
        return datetime.datetime.now().date().strftime("%B %d, %Y")

    def get_day(self):
        """Get current day of the week."""
        return datetime.datetime.now().strftime("%A")

    def convert_decimal_to_verbal(self, sentence):
        """Convert decimal numbers in a sentence to verbal form."""
        def replace_decimal(match):
            number = match.group(0)
            integer_part, decimal_part = number.split('.')
            return f"{integer_part} point {decimal_part}"

        return re.sub(r'\b\d+\.\d+\b', replace_decimal, sentence)

    def get_updated_system_info(self):
        """Get updated system information."""
        return get_system_info()

    def replace_symbols(self, expression):
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

    def get_intent_response(self, intent, response, replacement=None):
        """Get the response for an intent, with optional replacement."""
        if replacement:
            response = response.replace("{string}", replacement)
        self.prev_tag = intent["tag"]
        self.prev_response = response
        self.response = response

    def stop_audio(self):
        """Stop current audio playback and remove the output file if exists."""
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            if self.output_path and os.path.exists(self.output_path):
                os.remove(self.output_path)

    def stopping(self):
        """Stop current audio playback and return the stop response."""
        if self.play_obj and self.play_obj.is_playing():
            self.stop_response = self.prev_response
            self.play_obj.stop()
            self.stopped = True
            if self.output_path and os.path.exists(self.output_path):
                os.remove(self.output_path)
            return self.stop_response
        self.stopped = False

    def clean_input(self, user_input):
        """Clean the user input by converting decimal points and removing commas."""
        cleaned_input = re.sub(r"(\d+)\.(\d+)", r"\1 point \2", user_input)
        return re.sub(r'(?<=\d),(?=\d)', '', cleaned_input)

    def detect_wake_word(self, transcription):
        """Detect if the wake word 'edith' is present in the transcription."""
        return "edith" in transcription.lower()

    def clean_text(self, text):
        """Clean text by correcting misspelled words."""
        d = enchant.Dict("en_US")
        words = text.split()
        cleaned_words = []

        for word in words:
            if d.check(word):
                cleaned_words.append(word)
            else:
                suggestions = d.suggest(word)
                if suggestions:
                    cleaned_words.append(suggestions[0])
        return " ".join(cleaned_words)

    def Operational_Matrix(self):
        """Main loop for handling user input and generating responses."""
        while True:
            try:
                # Simulate user input (replace with actual audio capture and transcription)
                transcription = input("Enter transcript:").lower().strip()

                transcription = self.clean_text(transcription).lower()

                print("User input:", transcription)

                if self.detect_wake_word(transcription):
                    print("Wake word Detected...")
                    self.is_in_conversation = True
                    self.last_interaction_time = datetime.datetime.now()

                if (
                    self.is_in_conversation and 
                    (datetime.datetime.now() - self.last_interaction_time).total_seconds() < self.conversation_timeout
                ):
                    if transcription.lower() == "edith":
                        self.stopping()
                        transcription = 'edith'
                    else:
                        transcription = transcription.replace("edith", "")

                    tag, prob = self.classify_intent(transcription)
                    print("User input:", transcription)
                    print(prob)

                    if prob > 0.9999:
                        intent_found = False
                        for intent in self.intents["intents"]:
                            if tag == intent["tag"]:
                                print("Intent matched:", tag)
                                intent_found = True
                                self.handle_intent(intent, transcription)
                                break
                        if not intent_found:
                            self.response = None
                    else:
                        self.response = None
                        print("Confidence below threshold. Using LLM.")

                    if self.response:
                        self.stop_audio()
                        self.response = self.convert_decimal_to_verbal(self.response)
                        self.response = re.sub(r'(?<=\d),(?=\d)', '', self.response)
                        self.response = self.replace_symbols(self.response)
                        self.thread, self.play_obj, self.output_path = text_to_speech(self.response)
                    else:
                        self.stop_audio()
                        response = handle_conversation(transcription)
                        response = re.sub(r'(?<=\d),(?=\d)', '', response)
                        response = self.convert_decimal_to_verbal(response)
                        response = self.replace_symbols(response)
                        self.thread, self.play_obj, self.output_path = text_to_speech(response)

                    if self.response is None:
                        self.dialogue_manager.save_dialogue_archive(transcription, response)
                        self.dialogue_manager.backup_dialogue_archive()
                    else:
                        self.dialogue_manager.save_dialogue_archive(transcription, self.response)
                        self.dialogue_manager.backup_dialogue_archive()
                else:
                    self.is_in_conversation = False

            except Exception as e:
                logging.error("An error occurred: %s", e)

    def handle_intent(self, intent, user_input=None):
        """Handle the intent based on the tag and generate the appropriate response."""
        responses = {
            # "repeat_tsk": self.handle_repeat_tsk,
            "system_info_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]), self.get_updated_system_info()),
            "storage_info_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]), generate_storage_status_response(get_system_info())),
            "cpu_usage_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]), generate_cpu_usage_response(get_system_info())),
            "memory_usage_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]), generate_memory_usage_response(get_system_info())),
            "disk_space_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]), generate_disk_space_response(get_system_info())),
            "time_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{time}", self.get_time())),
            "date_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{date}", self.get_date())),
            "day_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{day}", self.get_day())),
            "ping_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", network_function(user_input))),
            "speedtest_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", download_speed_test())),
            "check_internet_tsk": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", check_internet())),
            "system_status": lambda: self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", get_live_system_status_response()))
        }
        if intent["tag"] in responses:
            responses[intent["tag"]]()
        else:
            self.get_intent_response(intent, random.choice(intent["responses"]))

    # def handle_repeat_tsk(self):
    #     """Handle 'repeat_tsk' intent."""
    #     if self.stopped:
    #         if self.prev_tag == "repeat_tsk":
    #             self.get_intent_response(self.prev_response)
    #         else:
    #             self.get_intent_response(f"{random.choice(self.intents['repeat_tsk']['responses'])} {self.stop_response}")
    #         self.stop_response = ""
    #         self.stopped = False
    #     elif self.prev_tag == "repeat_tsk":
    #         self.get_intent_response(self.prev_response)
    #     else:
    #         self.get_intent_response(f"{random.choice(self.intents['repeat_tsk']['responses'])} {self.prev_response}")

if __name__ == "__main__":
    intents_model = Edith_Mainframe(
        "scripts/edith/data/intents.json",
        "scripts/edith/data/data.pth"
    )

    while True:
        try:
            intents_model.Operational_Matrix()
        except Exception as e:
            logging.error("An error occurred in main loop: %s", e)
