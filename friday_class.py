import re
import random
import datetime
import json
import torch
import os
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from functions.opinion import opinion
from functions.system_info import *
from functions._math import *


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
        self.prev_input = ""
        self.prev_response = ""

    def is_complex_alphabetical_math_problem(self, user_input):
        # Regular expression to check for complex alphabetical math problems or expressions
        alphabetic_math_pattern = r"(?i)\b(?:what is the|evaluate the)?\s*(?:sum of|difference between|product of|square of|cube of)?\s*(?:zero|one|two|three|four|five|six|seven|eight|nine|ten)\b\s*(?:plus|minus|times|multiplied by|divided by|\+|\-|\*|\/|\^|and)\s*\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten)\b"

        # Check if the input string matches the complex alphabetical math pattern
        if re.search(alphabetic_math_pattern, user_input):
            return True
        else:
            return False

    def get_tag_from_response(self, response):
        # Find the tag associated with the given response in the intents
        for intent in self.intents["intents"]:
            if response in intent["responses"]:
                return intent["tag"]
        return None

    def get_time(self):
        time_ = datetime.datetime.now().time().strftime("%I:%M %p")
        if "PM" in time_:
            time_ = time_.replace("PM", "P M")
        elif "AM" in time_:
            time_ = time_.replace("AM", "A M")
        else:
            pass
        return time_

    def get_date(self):
        date_ = datetime.datetime.now().date().strftime("%B %d, %Y")
        return date_

    def get_day(self):
        day_ = datetime.datetime.now().strftime("%A")
        return day_

    def get_updated_system_info(self):
        return get_system_info()

    def process_user_input(self, user_input):
        return user_input.lower()

    def get_intent_response(self, intent, response, replacement=None):
        if replacement:
            response = response.replace("{string}", replacement)
        text_to_speech(response)
        print(intent["tag"])
        self.prev_tag = intent["tag"]
        self.prev_response = response

    def MainFrame(self, user_input):
        user_input = input("friday is active: ")
        user_input = self.process_user_input(user_input)
        info_system = self.get_updated_system_info()
        system_info = generate_system_status_response(info_system)
        storage_info = generate_storage_status_response(info_system)
        cpu_usage = generate_cpu_usage_response(info_system)
        memory_usage = generate_memory_usage_response(info_system)
        disk_space = generate_disk_space_response(info_system)
        if user_input.lower() == self.prev_input.lower():
            tag = "repeat_string"
        elif self.prev_tag == "technical":
            pass
        else:
            sentence = tokenize(user_input)
            X = bag_of_words(sentence, self.all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X)
            output = self.model(X)
            _, predicted = torch.max(output, dim=1)
            tag = self.tags[predicted.item()]
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
        if self.is_complex_alphabetical_math_problem(user_input):
            for intent in self.intents["intents"]:
                if intent["tag"] == "math":
                    response = random.choice(intent["responses"])
                    answer = solve_word_math_expression(user_input)
                    response = response.replace("{answer}", answer)
                    text_to_speech(response)
        elif prob.item() > 0.80:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:
                    if intent["tag"] == "repeat":
                        response = random.choice(intent["responses"])
                        text_to_speech(f"{response} {self.prev_response}")
                        print(intent["tag"])
                    elif intent["tag"] == "repeat_string":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response)
                    elif intent["tag"] == "system_info":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, system_info)
                    elif intent["tag"] == "storage_info":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, storage_info)
                    elif intent["tag"] == "cpu_usage":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, cpu_usage)
                    elif intent["tag"] == "memory_usage":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, memory_usage)
                    elif intent["tag"] == "disk_space":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, disk_space)
                    elif intent["tag"] == "opinion":
                        response = opinion(user_input)
                        self.get_intent_response(intent, response)
                    elif intent["tag"] == "time":
                        response = random.choice(intent["responses"]).replace(
                            "{time}", self.get_time()
                        )
                        self.get_intent_response(intent, response)
                    elif intent["tag"] == "date":
                        response = random.choice(intent["responses"]).replace(
                            "{date}", self.get_date()
                        )
                        self.get_intent_response(intent, response)
                    elif intent["tag"] == "day":
                        response = random.choice(intent["responses"]).replace(
                            "{day}", self.get_day()
                        )
                        self.get_intent_response(intent, response)
                    else:
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response)
            self.prev_input = user_input.lower()
        else:
            for intent in self.intents["intents"]:
                if intent["tag"] == "technical":
                    response = random.choice(intent["responses"])
                    text_to_speech(response)
                    print(intent["tag"])
                    break


if __name__ == "__main__":
    assistant = Friday()
    assistant.MainFrame()
