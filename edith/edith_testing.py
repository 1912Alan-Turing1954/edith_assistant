# import datetime
# import re
# import subprocess
# import random
# import torch
# import json
# import speech_recognition as sr

# from brain.model import NeuralNet
# from brain.nltk_utils import bag_of_words, tokenize

# # from system.file_fucntion import file_function
# from jenny_tts import text_to_speech, play_obj, output_path

# # from AI.test import edith_ai

# from system.system_info import *
# from system.network_tools import *


# class Friday:
#     def __init__(self):
#         with open("edith/data/intents.json", "r") as json_data:
#             self.intents = json.load(json_data)

#         FILE = "data/data.pth"
#         data = torch.load(FILE)

#         self.all_words = data["all_words"]
#         self.tags = data["tags"]
#         input_size = data["input_size"]
#         hidden_size = data["hidden_size"]
#         output_size = data["output_size"]
#         model_state = data["model_state"]

#         self.model = NeuralNet(input_size, hidden_size, output_size)
#         self.model.load_state_dict(model_state)
#         self.model.eval()

#         self.prev_tag = ""
#         self.prev_response = ""
#         self.num = 3
#         self.last_response = []

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
#         response = self.clean_input(response)

#         print(intent["tag"])
#         self.prev_tag = intent["tag"]
#         self.prev_response = response
#         text_to_speech(response)

#     def clean_input(self, user_input):
#         # Define a regex pattern to match dots between two numbers
#         pattern = r"(\d+)\.(\d+)"

#         # Replace dots with " point " only if they match the pattern
#         cleaned_input = re.sub(pattern, r"\1 point \2", user_input)
#         if "AI" in cleaned_input:
#             cleaned_input = cleaned_input.replace("AI", "A-I")

#         return cleaned_input

#     def MainFrame(self):
#         while True:
#             try:
#                 user_input = input("Friday is active: ")

#                 user_input = self.clean_input(user_input)

#                 sentence = tokenize(user_input)
#                 X = bag_of_words(sentence, self.all_words)
#                 X = X.reshape(1, X.shape[0])
#                 X = torch.from_numpy(X)
#                 output = self.model(X)
#                 _, predicted = torch.max(output, dim=1)
#                 tag = self.tags[predicted.item()]
#                 probs = torch.softmax(output, dim=1)
#                 prob = probs[0][predicted.item()]

#                 if prob.item() > 0.95:
#                     for intent in self.intents["intents"]:
#                         if tag == intent["tag"]:
#                             if intent["tag"] == "background_acknowledgment":
#                                 pass
#                             elif intent["tag"] == "mute_command_tsk":
#                                 self.mute = True
#                                 pass
#                             elif intent["tag"] == "repeat_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent, f"{response} {self.prev_response}"
#                                 )
#                             elif intent["tag"] == "repeat_string":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(intent, response)

#                             elif intent["tag"] == "system_info_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent,
#                                     response,
#                                     self.get_updated_system_info(),
#                                 )
#                             elif intent["tag"] == "storage_info_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent,
#                                     response,
#                                     generate_storage_status_response(get_system_info()),
#                                 )
#                             elif intent["tag"] == "cpu_usage_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent,
#                                     response,
#                                     generate_cpu_usage_response(get_system_info()),
#                                 )
#                             elif intent["tag"] == "memory_usage_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent,
#                                     response,
#                                     generate_memory_usage_response(get_system_info()),
#                                 )
#                             elif intent["tag"] == "disk_space_tsk":
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(
#                                     intent,
#                                     response,
#                                     generate_disk_space_response(get_system_info()),
#                                 )
#                             elif intent["tag"] == "time_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{time}", self.get_time()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             elif intent["tag"] == "date_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{date}", self.get_date()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             elif intent["tag"] == "day_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{day}", self.get_day()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             elif intent["tag"] == "ping_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{string}", network_function(user_input)
#                                 )
#                                 self.get_intent_response(intent, response)

#                             elif intent["tag"] == "speedtest_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{string}", download_speed_test()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             elif intent["tag"] == "check_internet_tsk":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{string}", check_internet()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             elif intent["tag"] == "system_status":
#                                 response = random.choice(intent["responses"]).replace(
#                                     "{string}", get_live_system_status_response()
#                                 )
#                                 self.get_intent_response(intent, response)
#                             else:
#                                 response = random.choice(intent["responses"])
#                                 self.get_intent_response(intent, response)
#                 else:
#                     try:
#                         # response = edith_ai(user_input)
#                         # if response is None:
#                         #     for intent in self.intents["intents"]:
#                         #         if intent["tag"] == "technical":
#                         #             response = random.choice(intent["responses"])
#                         #             text_to_speech(response)
#                         #             break
#                         # else:
#                         #     text_to_speech(response)
#                         print("ai response")
#                     except Exception as e:
#                         print("An error occurred:", e)

#             except Exception as e:
#                 print("An error occurred:", e)
#                 continue  # Restart the loop upon encountering an error


# if __name__ == "__main__":
#     assistant = Friday()
#     assistant.MainFrame()

import os
import shutil
import threading
import time
import datetime
import re
import random
import torch
import json
import subprocess
import speech_recognition as sr

from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize

from jenny_tts import (
    text_to_speech,
)  # Importing modified text_to_speech function

from modules.system_info import *
from modules.network_tools import *


class Friday:
    def __init__(self):
        with open("edith/data/intents.json", "r") as json_data:
            self.intents = json.load(json_data)

        FILE = "data/data.pth"
        data = torch.load(FILE)

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
        self.num = 3

        self.play_obj = None
        self.output_path = None

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
        response = self.clean_input(response)

        print(intent["tag"])
        self.prev_tag = intent["tag"]
        self.prev_response = response

        # Ensure previous audio playback is stopped and cleaned up
        self.stop_audio()
        # Play new audio response
        self.thread, self.play_obj, self.output_path = text_to_speech(response)

    def stop_audio(self):
        # Stop current audio playback if it's active
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()

        # Clean up: Optionally delete the previous audio file
        if self.output_path and os.path.exists(self.output_path):
            os.remove(self.output_path)

    def clean_input(self, user_input):
        # Define a regex pattern to match dots between two numbers
        pattern = r"(\d+)\.(\d+)"

        # Replace dots with " point " only if they match the pattern
        cleaned_input = re.sub(pattern, r"\1 point \2", user_input)
        if "AI" in cleaned_input:
            cleaned_input = cleaned_input.replace("AI", "A-I")

        return cleaned_input

    def MainFrame(self):
        while True:
            try:
                user_input = input("Friday is active: ")

                user_input = self.clean_input(user_input)
                # Handle pausing and resuming audio
                if "edith" == user_input.lower():
                    self.stop_audio()

                sentence = tokenize(user_input)
                X = bag_of_words(sentence, self.all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X)
                output = self.model(X)
                _, predicted = torch.max(output, dim=1)
                tag = self.tags[predicted.item()]
                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]

                if prob.item() > 0.95:
                    for intent in self.intents["intents"]:
                        if tag == intent["tag"]:
                            if intent["tag"] == "background_acknowledgment":
                                pass
                            elif intent["tag"] == "mute_command_tsk":
                                self.mute = True
                                pass
                            elif intent["tag"] == "repeat_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent, f"{response} {self.prev_response}"
                                )
                            elif intent["tag"] == "repeat_string":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)

                            elif intent["tag"] == "system_info_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent,
                                    response,
                                    self.get_updated_system_info(),
                                )
                            elif intent["tag"] == "storage_info_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent,
                                    response,
                                    generate_storage_status_response(get_system_info()),
                                )
                            elif intent["tag"] == "cpu_usage_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent,
                                    response,
                                    generate_cpu_usage_response(get_system_info()),
                                )
                            elif intent["tag"] == "memory_usage_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent,
                                    response,
                                    generate_memory_usage_response(get_system_info()),
                                )
                            elif intent["tag"] == "disk_space_tsk":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(
                                    intent,
                                    response,
                                    generate_disk_space_response(get_system_info()),
                                )
                            elif intent["tag"] == "time_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{time}", self.get_time()
                                )
                                self.get_intent_response(intent, response)
                            elif intent["tag"] == "date_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{date}", self.get_date()
                                )
                                self.get_intent_response(intent, response)
                            elif intent["tag"] == "day_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{day}", self.get_day()
                                )
                                self.get_intent_response(intent, response)
                            elif intent["tag"] == "ping_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{string}", network_function(user_input)
                                )
                                self.get_intent_response(intent, response)

                            elif intent["tag"] == "speedtest_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{string}", download_speed_test()
                                )
                                self.get_intent_response(intent, response)
                            elif intent["tag"] == "check_internet_tsk":
                                response = random.choice(intent["responses"]).replace(
                                    "{string}", check_internet()
                                )
                                self.get_intent_response(intent, response)
                            elif intent["tag"] == "system_status":
                                response = random.choice(intent["responses"]).replace(
                                    "{string}", get_live_system_status_response()
                                )
                                self.get_intent_response(intent, response)
                            else:
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)
                else:
                    try:
                        # response = edith_ai(user_input)
                        # if response is None:
                        #     for intent in self.intents["intents"]:
                        #         if intent["tag"] == "technical":
                        #             response = random.choice(intent["responses"])
                        #             text_to_speech(response)
                        #             break
                        # else:
                        #     text_to_speech(response)
                        print("ai response")
                    except Exception as e:
                        print("An error occurred:", e)

            except Exception as e:
                print("An error occurred:", e)
                continue  # Restart the loop upon encountering an error

    def stop(self):
        # Method to stop the assistant and clean up resources
        self.stop_audio()


# if __name__ == "__main__":
assistant = Friday()
edith = assistant.MainFrame()
