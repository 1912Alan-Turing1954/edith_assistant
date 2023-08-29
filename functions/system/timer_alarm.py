import json
import random
import re
import sys
import time

with open("./data/intents.json", "r") as data:
    intents = json.load(data)


# Function to set a timer
def set_timer(seconds):
    time.sleep(seconds)
    for intent in intents["intents"]:
        if intent["tag"] == "timer_done":
            response = random.choice(intents["response"])
            return response


def set_alarm(hour, minute, am_pm=None):
    print(hour, minute, am_pm)
    print(type(hour), type(minute), type(am_pm))  # Fixed the type checking

    current_time = time.localtime()

    if am_pm is None:
        am_pm = "AM" if current_time.tm_hour < 12 else "PM"

    if am_pm.lower() == "pm" and hour != 12:
        hour += 12
    elif am_pm.lower() == "am" and hour == 12:
        hour = 0

    # Create a struct_time object for the alarm time
    alarm_time = time.struct_time(
        (
            current_time.tm_year,
            current_time.tm_mon,
            current_time.tm_mday,
            hour,
            minute,
            0,  # seconds
            -1,  # weekday (not used)
            -1,  # yearday (not used)
            current_time.tm_isdst,
        )
    )

    # Calculate the time difference in seconds
    alarm_seconds = time.mktime(alarm_time) - time.mktime(current_time)

    # Ensure alarm_seconds is non-negative
    alarm_seconds = max(alarm_seconds, 0)

    time.sleep(alarm_seconds)
    for intent in intents["intents"]:
        if intent["tag"] == "alarm_done":
            response = random.choice(intents["response"])
            return response


def parse_time_units(command):
    time_units = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
    }

    total_seconds = 0

    for unit in time_units:
        pattern = r"(\d+)\s*" + unit
        matches = re.findall(pattern, command)

        if matches:
            for match in matches:
                total_seconds += int(match) * time_units[unit]

    return total_seconds if total_seconds > 0 else None


def parse_time(command):
    time_pattern = r"(\d{1,2}:\d{2})(?:\s*([apmAPM]{2}))?"
    hour_match = re.search(r"(\d{1,2})(?!\d)", command)
    hour_match_plus_ampm = re.search(
        r"(\d{1,2})\s*([apAP][mM])?|(\d{1,2})(?!\d)", command
    )
    match = re.search(time_pattern, command)

    if match:
        alarm_time = match.group(1)  # Use group(1) instead of groups()[0]
        am_pm = match.group(2)  # Use group(2) instead of groups()[1]
        hour, minute = alarm_time.split(":")

        if am_pm:
            return int(hour), int(minute), am_pm
        else:
            current_time = time.localtime()
            am_pm = "AM" if current_time.tm_hour < 12 else "PM"
            return int(hour), int(minute), am_pm

    elif (
        hour_match
        and len(hour_match.groups()) == 1
        and len(hour_match_plus_ampm.groups()) != 3
    ):
        # Handle cases where only the hour is provided (Assume "AM" as default)
        hour = int(hour_match.group(1))
        am_pm = "AM" if hour < 12 else "PM"
        return hour, 0, am_pm

    elif len(hour_match_plus_ampm.groups()) == 3:
        hour = int(hour_match_plus_ampm.group(1))  # Use group(1) instead of groups()[0]
        time_ = hour_match_plus_ampm.group(2)  # Use group(2) instead of groups()[1]
        return hour, 0, time_

    return None


# Listen to text-based commands
def set_timer_or_alarm(user_input):
    user_input = user_input.strip().lower()

    if "timer" in user_input:
        print(parse_time_units(user_input))
        seconds = parse_time_units(user_input)
        if seconds is not None:
            set_timer(seconds)
        else:
            pass

    elif "alarm" in user_input:
        alarm_time = parse_time(user_input)

        if alarm_time:
            hour, minute, am_pm = alarm_time
            set_alarm(hour, minute, am_pm)
        else:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <user_function_description>")
    else:
        _time_ = sys.argv[1]
        set_timer_or_alarm(_time_)
