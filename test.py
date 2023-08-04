import random
import datetime
import json, re, time
import threading
import torch
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from functions.opinion import opinion
from functions.system_info import *

with open('data/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

def get_time():
    time_ = datetime.datetime.now().time().strftime('%I:%M %p')
    if 'PM' in time_:
        time_ = time_.replace("PM", "P M")
    elif 'AM' in time_:
        time_ = time_.replace("AM", "A M")
    else:
        pass
    return time_
    
def get_date():
    date_ = datetime.datetime.now().date().strftime('%B %d, %Y')
    return date_

def get_day():
    day_ = datetime.datetime.now().strftime('%A')
    return day_

prev_tag = ""
prev_input = ""
prev_response = ""

list_of_words = [
    'and',
    'also',
    'as well as', 
    'along with'
]

def get_updated_system_info():
    return get_system_info()

def parse_time(user_input):
    # Regular expression patterns to match time-related phrases
    patterns = [
        r'(?P<value>\d+)\s*(?P<unit>seconds?)',
        r'(?P<value>\d+)\s*(?P<unit>minutes?)',
        r'(?P<value>\d+)\s*(?P<unit>hours?)',
        r'(?P<hour>\d+)\s*:\s*(?P<minute>\d+)\s*(?P<meridian>am|pm)'
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input.lower())
        if match:
            groups = match.groupdict()
            if 'unit' in groups:
                value = int(groups['value'])
                unit = groups['unit']
                if unit.startswith('hour'):
                    return value * 60 * 60
                elif unit.startswith('minute'):
                    return value * 60
                elif unit.startswith('second'):
                    return value
            elif 'hour' in groups:
                hour = int(groups['hour'])
                minute = int(groups['minute'])
                meridian = groups['meridian']
                if meridian == 'pm' and hour < 12:
                    hour += 12
                return datetime.timedelta(hours=hour, minutes=minute).seconds

    return None

def start_timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    text_to_speech(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")
    text_to_speech("Time's up!")

# Function to set an alarm
def set_alarm(alarm_time):
    current_time = datetime.datetime.now().time()
    if current_time >= alarm_time:
        alarm_time += datetime.timedelta(days=1)

    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= alarm_time:
            print("Alarm!")
            text_to_speech("Alarm!")
            break
        time.sleep(1)

# Function to handle background tasks (timers and alarms)
def handle_background_tasks(user_input):
    time_duration = parse_time(user_input)
    if time_duration:
        threading.Thread(target=start_timer, args=(time_duration,)).start()
    elif "set alarm" in user_input.lower():
        try:
            time_str = user_input.split("set alarm")[1].strip()
            alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            threading.Thread(target=set_alarm, args=(alarm_time,)).start()
        except ValueError:
            print("Please enter a valid time in the format HH:MM.")
            text_to_speech("Please enter a valid time in the format HH:MM.")

def chatbot_main():
    global prev_tag, prev_input, prev_response
    
    while True:
        user_input = input("friday is active: ")
        
        # Check for specific keywords to split input and process each part individually
        for word in list_of_words:
            if word in user_input.lower():
                # Split the user input based on the word "and"
                string_parts = user_input.lower().split(word)
                # Process each part of the user input individually
                for string_part in string_parts:
                    user_input_part = string_part.strip()
                    info_system = get_updated_system_info()
                    system_info = generate_system_status_response(info_system)
                    storage_info = generate_storage_status_response(info_system)
                    cpu_usage = generate_cpu_usage_response(info_system)
                    memory_usage = generate_memory_usage_response(info_system)
                    disk_space = generate_disk_space_response(info_system)
                    
                    if user_input_part.lower() == prev_input.lower():
                        tag = "repeat_string"
                    elif prev_tag == 'technical':
                        pass
                    else:
                        sentence = tokenize(user_input_part)
                        X = bag_of_words(sentence, all_words)
                        X = X.reshape(1, X.shape[0])
                        X = torch.from_numpy(X)
                        output = model(X)
                        _, predicted = torch.max(output, dim=1)
                        tag = tags[predicted.item()]
                        probs = torch.softmax(output, dim=1)
                        prob = probs[0][predicted.item()]
                    
                    if prob.item() > 0.80:
                        for intent in intents['intents']:
                            if tag == intent["tag"]:
                                if intent["tag"] == "repeat":
                                    response = random.choice(intent["responses"])
                                    text_to_speech(f"{response} {prev_response}")
                                    print(intent["tag"])
                                    break
                                elif intent["tag"] == "repeat_string":
                                    response = random.choice(intent["responses"])
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    break
                                elif intent["tag"] == "system_info":
                                    response = random.choice(intent["responses"])
                                    response = response.replace("{string}", str(system_info))
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "storage_info":
                                    response = random.choice(intent["responses"])
                                    response = response.replace("{string}", str(storage_info))
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "cpu_usage":
                                    response = random.choice(intent["responses"])
                                    response = response.replace("{string}", str(cpu_usage))
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "memory_usage":
                                    response = random.choice(intent["responses"])
                                    response = response.replace("{string}", str(memory_usage))
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "disk_space":
                                    response = random.choice(intent["responses"])
                                    response = response.replace("{string}", str(disk_space))
                                    text_to_speech(response)
                                    print(intent["tag"])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent['tag'] == 'opinion':
                                    text_to_speech(opinion(user_input_part))
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "time":
                                    response = random.choice(intent['responses']).replace("{time}", get_time())
                                    text_to_speech(response)
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "date":
                                    response = random.choice(intent['responses']).replace("{date}", get_date())
                                    text_to_speech(response)
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                elif intent["tag"] == "day":
                                    response = random.choice(intent['responses']).replace("{day}", get_day())
                                    text_to_speech(response)
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                                else:
                                    response = random.choice(intent['responses'])
                                    text_to_speech(response)
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                        prev_input = user_input_part.lower()
                        break
                    else:
                        for intent in intents['intents']:
                            if intent["tag"] == 'technical':
                                text_to_speech(random.choice(intent['responses']))
                                print(intent['tag'])
                                break
            else:
                info_system = get_updated_system_info()
                system_info = generate_system_status_response(info_system)
                storage_info = generate_storage_status_response(info_system)
                cpu_usage = generate_cpu_usage_response(info_system)
                memory_usage = generate_memory_usage_response(info_system)
                disk_space = generate_disk_space_response(info_system)
                
                if user_input.lower() == prev_input.lower():
                    tag = "repeat_string"
                elif prev_tag == 'technical':
                    pass
                elif "set alarm" in user_input.lower() or "start a timer for" in user_input.lower():
                    handle_background_tasks(user_input)
                    break
                else:
                    sentence = tokenize(user_input)
                    X = bag_of_words(sentence, all_words)
                    X = X.reshape(1, X.shape[0])
                    X = torch.from_numpy(X)
                    output = model(X)
                    _, predicted = torch.max(output, dim=1)
                    tag = tags[predicted.item()]
                    probs = torch.softmax(output, dim=1)
                    prob = probs[0][predicted.item()]
                
                if prob.item() > 0.785:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            if intent["tag"] == "repeat":
                                response = random.choice(intent["responses"])
                                text_to_speech(f"{response} {prev_response}")
                                print(intent["tag"])
                                break
                            elif intent["tag"] == "repeat_string":
                                response = random.choice(intent["responses"])
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                break
                            elif intent["tag"] == "system_info":
                                response = random.choice(intent["responses"])
                                response = response.replace("{string}", str(system_info))
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent["tag"] == "storage_info":
                                response = random.choice(intent["responses"])
                                response = response.replace("{string}", str(storage_info))
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent["tag"] == "cpu_usage":
                                response = random.choice(intent["responses"])
                                response = response.replace("{string}", str(cpu_usage))
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent["tag"] == "memory_usage":
                                response = random.choice(intent["responses"])
                                response = response.replace("{string}", str(memory_usage))
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent["tag"] == "disk_space":
                                response = random.choice(intent["responses"])
                                response = response.replace("{string}", str(disk_space))
                                text_to_speech(response)
                                print(intent["tag"])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent['tag'] == 'opinion':
                                text_to_speech(opinion(user_input))
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                            elif intent["tag"] == "time":
                                res_time = random.choice(intent['responses']).replace("{time}", get_time())
                                text_to_speech(res_time)
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = res_time
                                break
                            elif intent["tag"] == "date":
                                res_date = random.choice(intent['responses']).replace("{date}", get_date())
                                text_to_speech(res_date)
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = res_date
                                break
                            elif intent["tag"] == "day":
                                res_day = random.choice(intent['responses']).replace("{day}", get_day())
                                text_to_speech(res_day)
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = res_day
                                break
                            else:
                                response = random.choice(intent['responses'])
                                text_to_speech(response)
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                    prev_input = user_input.lower()
                    break
                else:
                    for intent in intents['intents']:
                        if intent["tag"] == 'technical':
                            text_to_speech(random.choice(intent['responses']))
                            print(intent['tag'])
                            break

# Start the chatbot in a separate thread
chatbot_thread = threading.Thread(target=chatbot_main)
chatbot_thread.start()

# Keep the main thread running indefinitely to allow timers/alarms and chatbot to run concurrently
while True:
    time.sleep(1)
