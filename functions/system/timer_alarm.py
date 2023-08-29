import re
import time
import threading


# Function to set a timer
def set_timer(seconds):
    print(f"Setting a timer for {seconds} seconds.")
    time.sleep(seconds)
    print("Timer is up!")


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

    print(f"Setting an alarm for {hour}:{minute} {am_pm}.")
    time.sleep(alarm_seconds)
    print("Alarm is ringing!")


# Function to parse time units
def parse_time_units(command):
    time_units = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
    }

    for unit in time_units:
        if unit in command:
            match = re.search(r"(\d+)\s*" + unit, command)
            if match:
                return int(match.group(1)) * time_units[unit]
    return None


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
def listen_for_commands():
    print("Enter a command (e.g., 'set timer 10 minutes' or 'set alarm 10:00 AM'):")
    command = input().lower()

    if "set timer" in command:
        seconds = parse_time_units(command)
        if seconds is not None:
            timer_thread = threading.Thread(target=set_timer, args=(seconds,))
            timer_thread.start()
        else:
            print("Invalid timer format. Please use 'set timer [number] [unit].'")

    elif "set alarm" in command:
        alarm_time = parse_time(command)

        if alarm_time:
            hour, minute, am_pm = alarm_time
            alarm_thread = threading.Thread(
                target=set_alarm, args=(hour, minute, am_pm)
            )
            alarm_thread.start()
        else:
            print(
                "Invalid alarm format. Please use 'set alarm [hour]:[minute] [AM/PM].'"
            )
