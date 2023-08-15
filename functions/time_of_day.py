import datetime
import random
import re
import json

with open("./data/intents.json", "r") as json_data:
    intents = json.load(json_data)


def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"


def time_of_day_correct(user_input):
    current_time_of_day = get_time_of_day()
    morning_patterns = []
    afternoon_patterns = []
    night_patterns = []

    for intent in intents["intents"]:
        if intent["tag"] == "good_morning":
            morning_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list
        elif intent["tag"] == "good_afternoon":
            afternoon_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list
        elif intent["tag"] == "good_night":
            night_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list

    response = None

    for pattern in morning_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "morning"
        ):
            response = f"Good morning, sir!"
            break

    for pattern in afternoon_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "afternoon"
        ):
            response = f"Good afternoon, sir!"
            break

    for pattern in night_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "night"
        ):
            response = f"Good night, sir!"
            break

    if response is None:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        for intent in intents["intents"]:
            if intent["tag"] == "day_correction":
                response = random.choice(intent["responses"]).format(
                    current_time=current_time
                )

    return response
