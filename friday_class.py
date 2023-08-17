import re
import random
import datetime
import json
import torch
import concurrent.futures
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from functions.opinion import opinion
from AI.flan_t5_large_model import generative_with_t5
from functions._math import solve_word_math_expression
from functions.time_of_day import time_of_day_correct
from functions.three_math_sim import create_simlulation_function
from functions.location import (
    get_address_description,
    get_location_description,
    get_long_and_lati,
)

from functions.system_info import (
    get_system_info,
    generate_system_status_response,
    generate_storage_status_response,
    generate_cpu_usage_response,
    generate_memory_usage_response,
    generate_disk_space_response,
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
        self.prev_input = ""
        self.prev_response = ""
        self.mute = False

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
        if self.mute:
            self.mute = False
            print("break_mute")
        else:
            pass

        print(type(user_input))
        user_input = user_input.lower()
        info_system = self.get_updated_system_info()
        system_info = generate_system_status_response(info_system)
        storage_info = generate_storage_status_response(info_system)
        cpu_usage = generate_cpu_usage_response(info_system)
        memory_usage = generate_memory_usage_response(info_system)
        disk_space = generate_disk_space_response(info_system)
        if user_input.lower() == self.prev_input.lower():
            tag = "repeat_string"
        elif (
            self.prev_tag == "technical" or self.prev_tag == "background_acknowledgment"
        ):
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
            result = solve_word_math_expression(user_input)
            for intent in self.intents["intents"]:
                if intent["tag"] == "math_tsk":
                    response = random.choice(intent["responses"]).format(answer=result)
                    text_to_speech(response)
                    print(intent["tag"])
                    print(response)
                    break
        elif prob.item() > 0.95:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:
                    if intent["tag"] == "background_acknowledgment":
                        continue
                    elif intent["tag"] == "mute_command":
                        self.mute = True
                        pass
                    elif intent["tag"] == "location_inquiry":
                        response = random.choice(intent["responses"])
                        response = get_location_description(response)
                        text_to_speech(response)
                    elif intent["tag"] == "simulate_interference":
                        response = user_input.lower()
                        text_to_speech("simulation initiated successfully")
                        with concurrent.futures.ThreadPoolExecutor(
                            max_workers=2
                        ) as executor:
                            # Run input processing and function conversion in parallel
                            future = executor.submit(
                                create_simlulation_function, response
                            )
                            # Wait for the future to complete
                            future.result()
                    elif intent["tag"] == "address_inquiry":
                        response = random.choice(intent["responses"])
                        response = get_address_description(response)
                        text_to_speech(response)
                    elif intent["tag"] == "repeat_tsk":
                        response = random.choice(intent["responses"])
                        text_to_speech(f"{response} {self.prev_response}")
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
                    elif intent["tag"] == "generative_with_t5":
                        response = random.choice(intent["responses"]).format(
                            string=generative_with_t5(user_input)
                        )
                        self.get_intent_response(intent, response)
                    elif intent["tag"] == "system_info_tsk":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, system_info)
                    elif intent["tag"] == "storage_info_tsk":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, storage_info)
                    elif intent["tag"] == "cpu_usage_tsk":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, cpu_usage)
                    elif intent["tag"] == "memory_usage_tsk":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, memory_usage)
                    elif intent["tag"] == "disk_space_tsk":
                        response = random.choice(intent["responses"])
                        self.get_intent_response(intent, response, disk_space)
                    elif intent["tag"] == "opinion":
                        response = opinion(user_input)
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
