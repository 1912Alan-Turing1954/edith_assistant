import re
import random
import datetime
import json
import subprocess
import torch
from word2number import w2n
import concurrent.futures
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from AI.flan_t5_large_model import generative_with_t5

# from functions.math._math import solve_word_math_expression
from functions.system.time_of_day import time_of_day_correct
from functions.system.maps.three_d_map import create_three_d_map
from functions.system.location import (
    get_address_description,
    get_location_description,
    get_long_and_lati,
    long,
    lat,
)

from functions.system.system_info import (
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
        self.task_tag_count = 0
        self.num = 3
        self.last_response = []
        self.mute = False

        self.follow_words = [
            " and then ",
            " and ",
            " also ",
            " and also ",
            " and by the way ",
            " additionally ",
        ]

    def follow_word_check(self, user_input):
        for word in self.follow_words:
            if word in user_input:
                return True
        return False

    def replace_follow_up_word(self, user_input):
        parts = [user_input]
        for word in self.follow_words:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(word))
            parts = new_parts

        # Print the split parts
        for part in parts:
            print(part.strip())  # .strip() to remove leading/trailing whitespace

        return parts

    def has_mathematical_function_or_x(self, user_input):
        # Define a regular expression pattern to match 'x' alone or mathematical expressions with 'x'
        pattern = r"\b[xX]\b|\b[xX]\b\s*[+\-*/^()\d\s]*"

        # Use re.search to find a match in the input string
        match = re.search(pattern, user_input)

        # If a match is found, return True, otherwise return False
        return bool(match)

    def convert_textual_numbers(self, user_input):
        words = user_input.lower().split()
        numerical_words = []

        for word in words:
            try:
                num = w2n.word_to_num(word)
                numerical_words.append(str(num))
            except ValueError:
                numerical_words.append(word)

        processed_input = " ".join(numerical_words)
        return processed_input.strip()

    def extract_function_from_input(self, user_input):
        for intent in self.intents["intents"]:
            if intent["tag"] == "simulate_interference_tsk":
                for pattern in intent["patterns"]:
                    if pattern.lower() in user_input:
                        user_input = user_input.replace(pattern, "")
                    else:
                        user_input = user_input.lower()

        replacements = {
            "cosine of x": "cos(x)",
            "sine of x": "sin(x)",
            "tangent of x": "tan(x)",
            "square root of x": "sqrt(x)",
            "logarithm base 10 of x": "log10(x)",
            "natural logarithm of x": "log(x)",
            "exponential of x": "exp(x)",
            "absolute value of x": "abs(x)",
            "cosine of y": "cos(y)",
            "sine of y": "sin(y)",
            "tangent of y": "tan(y)",
            "square root of y": "sqrt(y)",
            "logarithm base 10 of y": "log10(y)",
            "natural logarithm of y": "log(y)",
            "exponential of y": "exp(y)",
            "absolute value of y": "abs(y)",
            "x squared": "x**2",
            "x cubed": "x**3",
            "y squared": "y**2",
            "y cubed": "y**3",
            "equals": "==",
            "equal to": "==",
            "plus": "+",
            "minus": "-",
            "times": "*",
            "divided by": "/",
            "greater than": ">",
            "less than": "<",
            "not equal to": "!=",
        }
        for keyword, replacement in replacements.items():
            user_input = user_input.replace(keyword, replacement)
        return user_input.strip()

    def get_tag_from_response(self, response):
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
        user_input = user_input.lower()

    def get_intent_response(self, intent, response, replacement=None):
        if replacement:
            response = response.replace("{string}", replacement)
        text_to_speech(response)
        print(intent["tag"])
        self.prev_tag = intent["tag"]
        self.prev_response = response

    def MainFrame(self):
        while True:
            if self.mute:
                self.mute = False
                print("break_mute")
                pass
            else:
                pass

            user_input = input("friday is active: ")
            print(type(user_input))
            print(self.follow_word_check(user_input))

            print(
                self.has_mathematical_function_or_x(
                    self.extract_function_from_input(
                        self.convert_textual_numbers(user_input)
                    )
                )
            )

            if self.follow_word_check(user_input):
                string_parts = self.replace_follow_up_word(user_input)

                for string_part in string_parts:
                    user_input = string_part.lower()
                    info_system = self.get_updated_system_info()
                    system_info = generate_system_status_response(info_system)
                    storage_info = generate_storage_status_response(info_system)
                    cpu_usage = generate_cpu_usage_response(info_system)
                    memory_usage = generate_memory_usage_response(info_system)
                    disk_space = generate_disk_space_response(info_system)

                    if user_input == self.prev_input.lower():
                        tag = "repeat_string"
                    elif (
                        self.prev_tag == "technical"
                        or self.prev_tag == "background_acknowledgment"
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
                                    create_three_d_map(long, lat)

                                elif intent["tag"] == "show_location":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(intent, response)
                                    create_three_d_map(long, lat)

                                elif intent[
                                    "tag"
                                ] == "simulate_interference_tsk" and self.has_mathematical_function_or_x(
                                    self.extract_function_from_input(
                                        self.convert_textual_numbers(user_input)
                                    )
                                ):
                                    user_input = self.convert_textual_numbers(
                                        user_input
                                    )
                                    user_input = self.extract_function_from_input(
                                        user_input
                                    )
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
                                elif intent["tag"] == "generative_with_t5":
                                    response = random.choice(
                                        intent["responses"]
                                    ).format(string=generative_with_t5(user_input))
                                    self.get_intent_response(intent, response)
                                elif intent["tag"] == "system_info_tsk":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(
                                        intent, response, system_info
                                    )
                                elif intent["tag"] == "storage_info_tsk":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(
                                        intent, response, storage_info
                                    )
                                elif intent["tag"] == "cpu_usage_tsk":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(
                                        intent, response, cpu_usage
                                    )
                                elif intent["tag"] == "memory_usage_tsk":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(
                                        intent, response, memory_usage
                                    )
                                elif intent["tag"] == "disk_space_tsk":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(
                                        intent, response, disk_space
                                    )
                                elif intent["tag"] == "time_tsk":
                                    response = random.choice(
                                        intent["responses"]
                                    ).replace("{time}", self.get_time())
                                    self.get_intent_response(intent, response)
                                elif intent["tag"] == "date_tsk":
                                    response = random.choice(
                                        intent["responses"]
                                    ).replace("{date}", self.get_date())
                                    self.get_intent_response(intent, response)
                                elif intent["tag"] == "day_tsk":
                                    response = random.choice(
                                        intent["responses"]
                                    ).replace("{day}", self.get_day())
                                    self.get_intent_response(intent, response)
                                else:
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(intent, response)

                                if "tsk" in intent["tag"]:
                                    self.task_tag_count += 1
                                    if self.task_tag_count == self.num:
                                        for intent in self.intents["intents"]:
                                            if intent["tag"] == "anything_else_sir":
                                                response_tsk = random.choice(
                                                    intent["responses"]
                                                )
                                                self.last_response.append(response_tsk)
                                                self.task_tag_count = 0

                        self.prev_input = user_input.lower()

                    else:
                        for intent in self.intents["intents"]:
                            if intent["tag"] == "technical":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)
                                break

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
                                        pass

                        self.last_response.clear()

            else:
                user_input = user_input.lower()
                info_system = self.get_updated_system_info()
                system_info = generate_system_status_response(info_system)
                storage_info = generate_storage_status_response(info_system)
                cpu_usage = generate_cpu_usage_response(info_system)
                memory_usage = generate_memory_usage_response(info_system)
                disk_space = generate_disk_space_response(info_system)

                if user_input == self.prev_input.lower():
                    tag = "repeat_string"
                elif (
                    self.prev_tag == "technical"
                    or self.prev_tag == "background_acknowledgment"
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
                                create_three_d_map(long, lat)

                            elif intent["tag"] == "show_location":
                                response = random.choice(intent["responses"])
                                self.get_intent_response(intent, response)
                                create_three_d_map(long, lat)

                            elif intent[
                                "tag"
                            ] == "simulate_interference_tsk" and self.has_mathematical_function_or_x(
                                self.extract_function_from_input(
                                    self.convert_textual_numbers(user_input)
                                )
                            ):
                                user_input = self.convert_textual_numbers(user_input)
                                user_input = self.extract_function_from_input(
                                    user_input
                                )
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

                            if "tsk" in intent["tag"]:
                                self.task_tag_count += 1
                                if self.task_tag_count == self.num:
                                    for intent in self.intents["intents"]:
                                        if intent["tag"] == "anything_else_sir":
                                            response_tsk = random.choice(
                                                intent["responses"]
                                            )
                                            self.last_response.append(response_tsk)
                                            self.task_tag_count = 0

                    self.prev_input = user_input.lower()

                else:
                    for intent in self.intents["intents"]:
                        if intent["tag"] == "technical":
                            response = random.choice(intent["responses"])
                            self.get_intent_response(intent, response)
                            break

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
                                    self.num = 5
                                elif intent["tag"] == "anything_else_sir_no":
                                    response = random.choice(intent["responses"])
                                    self.get_intent_response(intent, response)
                                    print(self.num)
                                    self.num = self.num
                                else:
                                    pass

                    self.last_response.clear()


if __name__ == "__main__":
    assistant = Friday()
    assistant.MainFrame()
