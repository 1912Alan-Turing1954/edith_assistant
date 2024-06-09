import datetime
import subprocess
import random
import torch
import json

from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_function.tts import text_to_speech

# from AI.flan_t5_large_model import generative_with_t5
from functions.system.system_info import (
    get_system_info,
    generate_system_status_response,
    generate_storage_status_response,
    generate_cpu_usage_response,
    generate_memory_usage_response,
    generate_disk_space_response,
)
from functions.system.time_of_day import time_of_day_correct
from functions.system.maps.three_d_map import create_three_d_map
from functions.system.location import (
    get_address_description,
    get_location_description,
    get_long_and_lati,
    longitude,
    latitude,
)


class Friday:
    def __init__(self):
        with open("data/intents.json", "r") as json_data:
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
        self.last_response = []

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
        text_to_speech(response)
        print(intent["tag"])
        self.prev_tag = intent["tag"]
        self.prev_response = response

    def MainFrame(self):
        while True:
            user_input = input("Friday is active: ")

            if any(word in user_input for word in ["time", "date", "day"]):
                if "time" in user_input:
                    response = self.get_time()
                elif "date" in user_input:
                    response = self.get_date()
                elif "day" in user_input:
                    response = self.get_day()
                text_to_speech(response)
                continue

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
                        elif intent["tag"] == "location_inquiry_tsk":
                            response = random.choice(intent["responses"])
                            response = get_location_description(response)
                            self.get_intent_response(intent, response)
                        elif intent["tag"] == "address_inquiry_tsk":
                            response = random.choice(intent["responses"])
                            response = get_address_description(response)
                            self.get_intent_response(intent, response)
                        elif intent["tag"] == "coordinates_tsk":
                            response = random.choice(intent["responses"])
                            response = get_long_and_lati(response)
                            self.get_intent_response(intent, response)

                        elif intent["tag"] == "show_visualization" and (
                            self.prev_tag == "location_inquiry_tsk"
                            or self.prev_tag == "address_inquiry_tsk"
                            or self.prev_tag == "coordinates_tsk"
                        ):
                            response = random.choice(intent["responses"])
                            self.get_intent_response(intent, response)
                            create_three_d_map(longitude, latitude)

                        elif intent["tag"] == "show_location":
                            response = random.choice(intent["responses"])
                            self.get_intent_response(intent, response)
                            create_three_d_map(longitude, latitude)

                        elif intent["tag"] == "simulate_interference_tsk":
                            response = random.choice(intent["responses"])
                            self.get_intent_response(intent, response)
                            try:
                                subprocess.Popen(
                                    [
                                        "python",
                                        "./functions/math/math_sim.py",
                                        user_input,
                                    ]
                                )
                            except FileNotFoundError:
                                print("The script math_sim.py was not found.")
                                pass
                            except Exception as e:
                                print(e)
                                pass

                        elif intent["tag"] == "repeat_tsk":
                            response = random.choice(intent["responses"])
                            self.get_intent_response(
                                intent, f"{response} {self.prev_response}"
                            )
                        elif intent["tag"] == "repeat_string":
                            response = random.choice(intent["responses"])
                            self.get_intent_response(intent, response)
                        elif intent["tag"] == "good_morning":
                            response = time_of_day_correct(user_input)
                            self.get_intent_response(intent, response)
                        elif intent["tag"] == "good_afternoon":
                            response = time_of_day_correct(user_input)
                            self.get_intent_response(intent, response)
                        elif intent["tag"] == "good_night":
                            response = time_of_day_correct(user_input)
                            self.get_intent_response(intent, response)
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
                        else:
                            continue

                    if "tsk" in intent["tag"]:
                        self.num += 1
                        if self.num == self.num:
                            for intent in self.intents["intents"]:
                                if intent["tag"] == "anything_else_sir":
                                    response_tsk = random.choice(intent["responses"])
                                    self.last_response.append(response_tsk)
                                    self.num = 0

                self.prev_input = user_input.lower()

            else:
                response = generative_with_t5(user_input)  # Passing to generative AI
                text_to_speech(response)

            if self.last_response:
                text_to_speech(self.last_response[0])
                user_input = input("Yes / No: ")
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
                            if intent["tag"] == "anything_else_sir_yes":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)
                                print(intent["tag"])
                                self.num = 5
                            elif intent["tag"] == "anything_else_sir_no":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)
                                print(self.num)
                                self.num = self.num
                            else:
                                continue

                self.last_response.clear()


if __name__ == "__main__":
    assistant = Friday()
    assistant.MainFrame()
