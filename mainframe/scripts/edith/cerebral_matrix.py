# import datetime
# import glob
# import logging
# import pickle
# import re
# import shutil
# import torch
# import json

# from brain.model import NeuralNet
# from brain.nltk_utils import bag_of_words, tokenize

# from jenny_tts import text_to_speech  # Importing modified text_to_speech function

# from modules.system_info import *
# from modules.network_tools import *
# from speech_to_text import *
# import enchant


# # Assuming your Intent Classifier class and functions are defined here
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
#         self.dialogue_archive = (
#             "mainframe/scripts/data/database/archives/dialogue/dialogue_archives.bin"
#         )
#         self.backup_dir = "mainframe/scripts/data/database/archives/dialogue"

#         self.is_in_conversation = False  # Flag to track if in conversation
#         self.conversation_timeout = 5  # Timeout in seconds for conversation reset
#         self.last_interaction_time = datetime.datetime.now()

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

#     def LLM(self, user_input):
#         if user_input:
#             return "ai response"
#         else:
#             return

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

#     def get_updated_system_info(self):
#         return get_system_info()

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

#     def inturupt(self):
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

#         return cleaned_input

#     def save_dialogue_archive(self, user_input, bot_response):
#         chat_entry = {
#             "User": user_input,
#             "Bot": bot_response,
#             "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
#         }

#         # Append new entry to the existing binary file
#         with open(self.dialogue_archive, "ab") as file:
#             pickle.dump(chat_entry, file)

#     def backup_dialogue_archive(self):
#         # Ensure backup directory exists
#         os.makedirs(self.backup_dir, exist_ok=True)

#         # Search for existing backup files in backup directory
#         existing_backups = glob.glob(
#             os.path.join(self.backup_dir, "dialogue_archive_backup*.bin")
#         )

#         # Delete previous backup(s) if exist
#         for backup_file in existing_backups:
#             os.remove(backup_file)
#             print(f"Deleted previous backup: {backup_file}")

#         # Generate new backup file name
#         backup_file = os.path.join(
#             self.backup_dir,
#             f"dialogue_archive_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.bin",
#         )

#         # Copy current dialogue archive file to backup
#         shutil.copyfile(self.dialogue_archive, backup_file)
#         print(f"Backup created: {backup_file}")

#     def detect_wake_word(self, transcription):
#         # Implement your logic to detect the wake word ("Edith" in this case)
#         return "edith" in transcription.lower() or "test" in transcription.lower()

#     def clean_text(self, text):
#         # Create an English dictionary instance
#         d = enchant.Dict("en_US")

#         # Split text into words
#         words = text.split()

#         cleaned_words = []

#         # Iterate through each word and check if it's a valid English word
#         for word in words:
#             if d.check(word):  # Check if the word is valid
#                 cleaned_words.append(word)
#             else:
#                 # If the word is not valid, attempt to suggest a correction
#                 suggestions = d.suggest(word)
#                 if suggestions:
#                     cleaned_words.append(suggestions[0])  # Choose the first suggestion
#                 # If no suggestions are available, ignore the word

#         # Join the cleaned words back into a single string
#         cleaned_text = " ".join(cleaned_words)

#         return cleaned_text

#     def Operational_Matrix(self):
#         while True:
#             try:
#                 # audio = capture_audio()
#                 # transcription = speech_to_text(
#                     # audio
#                 # )  # Replace with your speech to text function

#                 transcription = input("Enter transcript:")
#                 transcription = self.clean_text(transcription.lower().strip())
#                 print("User input:", transcription)

#                 if self.detect_wake_word(transcription):
#                     print("Addressing Edith")
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
#                     tag, prob = self.classify_intent(transcription)
#                     print("Intent tag:", tag)

#                     if prob > 0.90:
#                         intent_found = False
#                         for intent in self.intents["intents"]:
#                             if tag == intent["tag"]:
#                                 intent_found = True
#                                 self.handle_intent(intent, transcription)
#                         if not intent_found:
#                             self.response = (
#                                 None  # Set response to None if no intent found
#                             )

#                     if self.response:
#                         self.stop_audio()
#                         self.thread, self.play_obj, self.output_path = text_to_speech(
#                             self.response
#                         )

#                     if self.response is None:
#                         self.stop_audio()
#                         response = self.LLM(transcription)
#                         self.thread, self.play_obj, self.output_path = text_to_speech(
#                             response
#                         )

#                     if self.response is None:
#                         self.save_dialogue_archive(transcription, response)
#                         self.backup_dialogue_archive()
#                     else:
#                         self.save_dialogue_archive(transcription, self.response)
#                         self.backup_dialogue_archive()
#                 else:
#                     # Conversation timeout or not in conversation state
#                     self.is_in_conversation = False

#             except Exception as e:
#                 logging.error("An error occurred: %s", e)

#     def handle_intent(self, intent, user_input=None):
#         if intent["tag"] == "repeat_tsk" and self.stopped:
#             if self.prev_tag == "repeat_tsk":
#                 self.get_intent_response(
#                     intent,
#                     f"{self.stop_response}",
#                 )
#             else:
#                 self.get_intent_response(
#                     intent,
#                     f"{random.choice(intent['responses'])} {self.stop_response}",
#                 )
#             self.stop_response = ""
#             self.stopped = False
#         elif intent["tag"] == "repeat_tsk":
#             if self.prev_tag == "repeat_tsk":
#                 print("previous tag is repeat_tsk")
#                 self.get_intent_response(
#                     intent,
#                     f"{self.prev_response}",
#                 )
#             else:
#                 print("previous tag is repeat_tsk")
#                 self.get_intent_response(
#                     intent,
#                     f"{random.choice(intent['responses'])} {self.prev_response}",
#                 )

#         elif intent["tag"] == "system_info_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]),
#                 self.get_updated_system_info(),
#             )
#         elif intent["tag"] == "storage_info_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]),
#                 generate_storage_status_response(get_system_info()),
#             )
#         elif intent["tag"] == "cpu_usage_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]),
#                 generate_cpu_usage_response(get_system_info()),
#             )
#         elif intent["tag"] == "memory_usage_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]),
#                 generate_memory_usage_response(get_system_info()),
#             )
#         elif intent["tag"] == "disk_space_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]),
#                 generate_disk_space_response(get_system_info()),
#             )
#         elif intent["tag"] == "time_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace("{time}", self.get_time()),
#             )
#         elif intent["tag"] == "date_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace("{date}", self.get_date()),
#             )
#         elif intent["tag"] == "day_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace("{day}", self.get_day()),
#             )
#         elif intent["tag"] == "ping_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace(
#                     "{string}", network_function(user_input)
#                 ),
#             )
#         elif intent["tag"] == "speedtest_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace(
#                     "{string}", download_speed_test()
#                 ),
#             )
#         elif intent["tag"] == "check_internet_tsk":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace(
#                     "{string}", check_internet()
#                 ),
#             )
#         elif intent["tag"] == "system_status":
#             self.get_intent_response(
#                 intent,
#                 random.choice(intent["responses"]).replace(
#                     "{string}", get_live_system_status_response()
#                 ),
#             )
#         else:
#             self.get_intent_response(intent, random.choice(intent["responses"]))


# if __name__ == "__main__":
#     intents_model = Edith_Mainframe(
#         "mainframe/scripts/edith/data/intents.json",
#         "mainframe/scripts/edith/data/data.pth",
#     )

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
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')


from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from jenny_tts import text_to_speech  # Assuming this import is correct
from modules.system_info import *  # Adjusted import to specific function
from modules.network_tools import *
# from speech_to_text import *
import enchant
# from mainframe.scripts.data.database.large_language_model.llm_ import llm
from data.database.large_language_model.llm_ import *

import sqlite3
import os
import datetime

class DialogueManager:
    def __init__(self, dialogue_archive, backup_dir):
        self.dialogue_archive = dialogue_archive
        self.backup_dir = backup_dir
        self._initialize_database()

    def _initialize_database(self):
        # Create SQLite database if not exists
        self.conn = sqlite3.connect(self.dialogue_archive)
        self.cursor = self.conn.cursor()

        # Create dialogue table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialogue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                bot_response TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def save_dialogue_archive(self, user_input, bot_response):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert new dialogue entry into the database
        self.cursor.execute('''
            INSERT INTO dialogue (user_input, bot_response, timestamp)
            VALUES (?, ?, ?)
        ''', (user_input, bot_response, timestamp))
        self.conn.commit()

    def backup_dialogue_archive(self):
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

        # Generate new backup file name
        backup_file = os.path.join(
            self.backup_dir,
            f"dialogue_archive_backup_.db",
        )

        # Copy current dialogue archive file to backup
        shutil.copyfile(self.dialogue_archive, backup_file)
        print(f"Backup created: {backup_file}")


class Edith_Mainframe(object):
    def __init__(self, intents_file, data_file):
        self.intents_file = intents_file
        self.data_file = data_file
        self.load_intents_and_model()

        self.prev_tag = ""
        self.prev_response = ""
        self.stop_response = ""

        self.play_obj = None
        self.output_path = None
        self.stopped = False
        self.response = None
        self.dialogue_archive = "mainframe/scripts/data/database/archives/dialogue/dialogue_archives.bin"
        self.backup_dir = "mainframe/scripts/data/database/archives/dialogue"

        self.is_in_conversation = False  # Flag to track if in conversation
        self.conversation_timeout = 60  # Timeout in seconds for conversation reset
        self.last_interaction_time = datetime.datetime.now()
        self.dialogue_manager = DialogueManager('mainframe/scripts/data/database/archives/dialogue/dialogue_archive.db', 'backup_dir')


    def load_intents_and_model(self):
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
        time_ = datetime.datetime.now().time().strftime("%I:%M %p")
        if "PM" in time_:
            time_ = time_.replace("PM", "P M")
        elif "AM" in time_:
            time_ = time_.replace("AM", "A M")
        return time_

    def get_date(self):
        date_ = datetime.datetime.now().date().strftime("%B %d, %Y")
        return date_

    def get_day(self):
        day_ = datetime.datetime.now().strftime("%A")
        return day_

    def convert_decimal_to_verbal(self, sentence):
    # Define a function to convert each decimal number
        def replace_decimal(match):
            number = match.group(0)
            # Split the number into integer and decimal parts
            integer_part, decimal_part = number.split('.')
            # Construct the verbal representation
            return f"{integer_part} point {decimal_part}"

        # Use a regular expression to find all decimal numbers in the sentence
        return re.sub(r'\b\d+\.\d+\b', replace_decimal, sentence)

    def get_updated_system_info(self):
        return get_system_info()

    def get_intent_response(self, intent, response, replacement=None):
        if replacement:
            response = response.replace("{string}", replacement)

        self.prev_tag = intent["tag"]
        self.prev_response = response
        self.response = response

    def stop_audio(self):
        # Stop current audio playback
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            if self.output_path and os.path.exists(self.output_path):
                os.remove(self.output_path)

    def stopping(self):
        # Stop current audio playback
        if self.play_obj and self.play_obj.is_playing():
            self.stop_response = self.prev_response
            self.play_obj.stop()
            self.stopped = True
            if self.output_path and os.path.exists(self.output_path):
                os.remove(self.output_path)
            return self.stop_response
        else:
            self.stopped = False

    def clean_input(self, user_input):
        pattern = r"(\d+)\.(\d+)"
        cleaned_input = re.sub(pattern, r"\1 point \2", user_input)
        return cleaned_input



    def detect_wake_word(self, transcription):
        return "edith" in transcription.lower()

    def clean_text(self, text):
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
        cleaned_text = " ".join(cleaned_words)
        return cleaned_text

    def Operational_Matrix(self):
        while True:
            try:
                # audio = capture_audio()
                # transcription = speech_to_text(
                    # audio
                # )  # Replace with your speech to text function

                transcription = input("Enter transcript:")
                transcription = self.clean_text(transcription.lower().strip())

                print("User input:", transcription)

                if self.detect_wake_word(transcription):
                    print("Edith Detected")
                    self.is_in_conversation = True
                    self.last_interaction_time = datetime.datetime.now()

                # Check if still within conversation timeout
                if (
                    self.is_in_conversation
                    and (
                        datetime.datetime.now() - self.last_interaction_time
                    ).total_seconds()
                    < self.conversation_timeout
                ):
                    if transcription.lower() == "edith":
                        self.stopping()
                        transcription = 'edith'
                    else:
                        transcription = transcription.lower().replace("edith", "")



                    tag, prob = self.classify_intent(transcription)

                    print("User input:", transcription)

                    print(prob)
                    # Adjust the confidence threshold as needed
                    if prob > 0.9995:
                        intent_found = False
                        for intent in self.intents["intents"]:
                            if tag == intent["tag"]:
                                print("Intent matched:", tag)
                                intent_found = True
                                self.handle_intent(intent, transcription)
                                break  # Exit loop once intent is found
                        if not intent_found:
                            self.response = None
                    else:
                        self.response = None
                        print("Confidence below threshold. Using LLM.")


                    if self.response:
                        self.stop_audio()
                        self.response = self.convert_decimal_to_verbal(self.response)
                        self.thread, self.play_obj, self.output_path = text_to_speech(self.response)

                    else:
                        self.stop_audio()
                        response = llm_main(transcription)
                        response = self.convert_decimal_to_verbal(response)
                        self.thread, self.play_obj, self.output_path = text_to_speech(
                            response
                        )

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
        if intent["tag"] == "repeat_tsk" and self.stopped:
            if self.prev_tag == "repeat_tsk":
                self.get_intent_response(intent, f"{self.stop_response}")
            else:
                self.get_intent_response(intent, f"{random.choice(intent['responses'])} {self.stop_response}")
            self.stop_response = ""
            self.stopped = False
        elif intent["tag"] == "repeat_tsk":
            if self.prev_tag == "repeat_tsk":
                print("previous tag is repeat_tsk")
                self.get_intent_response(intent, f"{self.prev_response}")
            else:
                print("previous tag is repeat_tsk")
                self.get_intent_response(intent, f"{random.choice(intent['responses'])} {self.prev_response}")
        elif intent["tag"] == "system_info_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]), self.get_updated_system_info())
        elif intent["tag"] == "storage_info_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]), generate_storage_status_response(get_system_info()))
        elif intent["tag"] == "cpu_usage_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]), generate_cpu_usage_response(get_system_info()))
        elif intent["tag"] == "memory_usage_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]), generate_memory_usage_response(get_system_info()))
        elif intent["tag"] == "disk_space_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]), generate_disk_space_response(get_system_info()))
        elif intent["tag"] == "time_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{time}", self.get_time()))
        elif intent["tag"] == "date_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{date}", self.get_date()))
        elif intent["tag"] == "day_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{day}", self.get_day()))
        elif intent["tag"] == "ping_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", network_function(user_input)))
        elif intent["tag"] == "speedtest_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", download_speed_test()))
        elif intent["tag"] == "check_internet_tsk":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", check_internet()))
        elif intent["tag"] == "system_status":
            self.get_intent_response(intent, random.choice(intent["responses"]).replace("{string}", get_live_system_status_response()))
        else:
            self.get_intent_response(intent, random.choice(intent["responses"]))


if __name__ == "__main__":
    intents_model = Edith_Mainframe("mainframe/scripts/edith/data/intents.json",
                                    "mainframe/scripts/edith/data/data.pth")

    while True:
        try:
            intents_model.Operational_Matrix()

        except Exception as e:
            logging.error("An error occurred in main loop: %s", e)

