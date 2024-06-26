import datetime
import glob
import pickle
import re
import shutil
import torch
import json

from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize

from jenny_tts import text_to_speech  # Importing modified text_to_speech function

from modules.system_info import *
from modules.network_tools import *


# Assuming your Intent Classifier class and functions are defined here
class Edith_Mainframe(object):
    def __init__(self, intents_file, data_file):
        with open(intents_file, "r") as json_data:
            self.intents = json.load(json_data)

        data = torch.load(data_file)
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size)
        self.model.load_state_dict(model_state)
        self.model.eval()

        self.prev_tag = ""
        self.prev_response = ""
        self.stop_response = ""

        self.play_obj = None
        self.output_path = None
        self.stopped = False
        self.response = None
        self.dialogue_archive = (
            "mainframe/scripts/data/database/archives/dialogue/dialogue_archives.bin"
        )
        self.backup_dir = "mainframe/scripts/data/database/archives/dialogue"

    def LLM(self, user_input):
        if user_input:
            return "ai response"
        else:
            return

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

    def inturupt(self):
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

    def save_dialogue_archive(self, user_input, bot_response):
        chat_entry = {
            "User": user_input,
            "Bot": bot_response,
            "Timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        }

        # Append new entry to the existing binary file
        with open(self.dialogue_archive, "ab") as file:
            pickle.dump(chat_entry, file)

    def backup_dialogue_archive(self):
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

        # Search for existing backup files in backup directory
        existing_backups = glob.glob(
            os.path.join(self.backup_dir, "dialogue_archive_backup*.bin")
        )

        # Delete previous backup(s) if exist
        for backup_file in existing_backups:
            os.remove(backup_file)
            print(f"Deleted previous backup: {backup_file}")

        # Generate new backup file name
        backup_file = os.path.join(
            self.backup_dir,
            f"dialogue_archive_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.bin",
        )

        # Copy current dialogue archive file to backup
        shutil.copyfile(self.dialogue_archive, backup_file)
        print(f"Backup created: {backup_file}")

    def Matrix(self):
        while True:
            try:
                print(self.stop_response)
                print(self.prev_response)

                user_input = input("Friday is active: ")

                tag, prob = self.classify_intent(user_input)

                if "edith" == user_input.lower():
                    self.inturupt()
                elif prob > 0.90:
                    for intent in self.intents["intents"]:
                        if tag == intent["tag"]:
                            if intent["tag"] == "repeat_tsk" and self.stopped:

                                self.stopped = True

                if prob > 0.90:
                    intent_found = False
                    for intent in self.intents["intents"]:
                        if tag == intent["tag"]:
                            intent_found = True
                            if intent["tag"] == "repeat_tsk" and self.stopped:
                                self.get_intent_response(
                                    intent,
                                    f"{random.choice(intent['responses'])} {self.stop_response}",
                                )
                                self.stop_response = ""
                                self.stopped = False
                            elif intent["tag"] == "repeat_tsk":
                                self.get_intent_response(
                                    intent,
                                    f"{random.choice(intent['responses'])} {self.prev_response}",
                                )
                            elif intent["tag"] == "system_info_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]),
                                    get_live_system_status_response(
                                        self.get_updated_system_info()
                                    ),
                                )
                            elif intent["tag"] == "storage_info_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]),
                                    generate_storage_status_response(get_system_info()),
                                )
                            elif intent["tag"] == "cpu_usage_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]),
                                    generate_cpu_usage_response(get_system_info()),
                                )
                            elif intent["tag"] == "memory_usage_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]),
                                    generate_memory_usage_response(get_system_info()),
                                )
                            elif intent["tag"] == "disk_space_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]),
                                    generate_disk_space_response(get_system_info()),
                                )
                            elif intent["tag"] == "time_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{time}", self.get_time()
                                    ),
                                )
                            elif intent["tag"] == "date_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{date}", self.get_date()
                                    ),
                                )
                            elif intent["tag"] == "day_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{day}", self.get_day()
                                    ),
                                )
                            elif intent["tag"] == "ping_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{string}", network_function(user_input)
                                    ),
                                )
                            elif intent["tag"] == "speedtest_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{string}", download_speed_test()
                                    ),
                                )
                            elif intent["tag"] == "check_internet_tsk":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{string}", check_internet()
                                    ),
                                )
                            elif intent["tag"] == "system_status":
                                self.get_intent_response(
                                    intent,
                                    random.choice(intent["responses"]).replace(
                                        "{string}", get_live_system_status_response()
                                    ),
                                )
                            else:
                                self.get_intent_response(
                                    intent, random.choice(intent["responses"])
                                )
                    if not intent_found:
                        self.response = None  # Set response to None if no intent found

                if self.response:
                    self.stop_audio()

                    self.thread, self.play_obj, self.output_path = text_to_speech(
                        self.response
                    )
                if self.response is None:
                    self.stop_audio()

                    response = self.LLM(user_input)

                    self.thread, self.play_obj, self.output_path = text_to_speech(
                        response
                    )

                if self.response is None:
                    self.save_dialogue_archive(user_input, response)
                    self.backup_dialogue_archive()
                else:
                    self.save_dialogue_archive(user_input, self.response)
                    self.backup_dialogue_archive()

            except Exception as e:
                print("An error occurred:", e)


while True:
    intents_model = Edith_Mainframe(
        "mainframe/scripts/edith/data/intents.json",
        "mainframe/scripts/edith/data/data.pth",
    )

    intents_model.Matrix()
