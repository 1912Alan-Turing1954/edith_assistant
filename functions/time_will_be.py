# from datetime import datetime, timedelta
# import re
# import nltk
# from nltk.tokenize import word_tokenize

# nltk.download("punkt")


# def calculate_future_time(base_time, hours, minutes):
#     future_time = base_time + timedelta(hours=hours, minutes=minutes)
#     return future_time


# def extract_time_from_string(input_string):
#     tokens = word_tokenize(input_string.lower())
#     time_pattern = r"(\d+)(?::(\d+))?\s?(o'clock|am|pm)?"

#     for token in tokens:
#         if re.match(time_pattern, token):
#             time_match = re.match(time_pattern, token)
#             given_hour = int(time_match.group(1))
#             given_minute = int(time_match.group(2)) if time_match.group(2) else 0
#             given_period = time_match.group(3)
#             return given_hour, given_minute, given_period

#     return None, None, None


# def calculate_future_time_from_input(user_input):
#     current_time = datetime.now()

#     given_hour, given_minute, given_period = extract_time_from_string(user_input)
#     future_hours = (
#         given_hour if given_hour is not None else extract_hours_from_string(user_input)
#     )
#     future_minutes = given_minute

#     if future_hours is not None:
#         future_time = calculate_future_time(current_time, future_hours, future_minutes)
#         return f"In {future_hours} hours and {future_minutes} minutes from now, it will be: {future_time.strftime('%I:%M %p')}"
#     elif given_hour is not None:
#         if given_period:
#             if given_period == "pm" and given_hour != 12:
#                 given_hour += 12
#             elif given_period == "am" and given_hour == 12:
#                 given_hour = 0

#         given_time = current_time.replace(
#             hour=given_hour, minute=given_minute, second=0, microsecond=0
#         )
#         future_time = calculate_future_time(
#             given_time, 2, 0
#         )  # Assuming 2 hours from the given time
#         return f"In 2 hours from {given_time.strftime('%I:%M %p')}, it will be: {future_time.strftime('%I:%M %p')}"

#     else:
#         return "Invalid input format. Please use a valid format like 'What time will it be in 2 hours and 10 minutes?' or '2 o'clock pm after 3 hours and 15 minutes.'"


# # Test the function with different inputs
# input1 = "What time will it be 2 hours and 0 minutes from 10 o'clock?"
# input2 = "What time will it be in 3 hours and 0 minutes?"
# print(calculate_future_time_from_input(input1))
# print(calculate_future_time_from_input(input2))
