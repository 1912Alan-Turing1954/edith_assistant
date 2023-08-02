import random
import datetime
import json
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

prev_tag = ""
prev_input = ""
prev_response = ""

def get_updated_system_info():
    return get_system_info()

class Friday():
    
    def __init__(self):
        self.empty = ""
        self.list_of_words = [
            'and',
            'also',
            'as well as'    
            'along with'
        ]

    def get_time(self):
        time_ = datetime.datetime.now().time().strftime('%I:%M %p')
        if 'PM' in time_:
            time_ = time_.replace("PM", "P M")
        elif 'AM' in time_:
            time_ = time_.replace("AM", "A M")
        else:
            pass
        return time_
    
    def Main(self, user_input):
        global prev_tag, prev_input, prev_response
            
        for word in self.list_of_words:
            if word in user_input.lower():
                # Split the user input based on the word "and"
                string_parts = user_input.lower().split(word)
                # Process each part of the user input individually
                for string_part in string_parts:
                    
                    user_input_part = string_part.strip()
                    system_info = get_updated_system_info()
                    storage_info = generate_storage_status_response(system_info)
                    cpu_usage = generate_cpu_usage_response(system_info)
                    memory_usage = generate_memory_usage_response(system_info)
                    disk_space = generate_disk_space_response(system_info)
                        
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
                                    text_to_speech(opinion(user_input_part))
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                            
                                elif intent["tag"] == "time":
                                    res_time = random.choice(intent['responses']).replace("{time}", self.get_time())
                                    text_to_speech(f"{res_time}")
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = res_time
                                    break
                            
                                else:
                                    response = random.choice(intent['responses'])
                                    text_to_speech(f"{response}")
                                    print(intent['tag'])
                                    prev_tag = intent['tag']
                                    prev_response = response
                                    break
                        
                        prev_input = user_input_part.lower()
                        break
                    
                    else:
                            for intent in intents['intents']:
                                if intent["tag"] == 'technical':
                                    text_to_speech(f"{random.choice(intent['responses'])}")
                                    print(intent['tag'])
                                    break
            else:
                system_info = get_updated_system_info()
                storage_info = generate_storage_status_response(system_info)
                cpu_usage = generate_cpu_usage_response(system_info)
                memory_usage = generate_memory_usage_response(system_info)
                disk_space = generate_disk_space_response(system_info)
                
                if user_input.lower() == prev_input.lower():
                    tag = "repeat_string"
                
                elif prev_tag == 'technical':
                    pass
                
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
                                res_time = random.choice(intent['responses']).replace("{time}", self.get_time())
                                text_to_speech(f"{res_time}")
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = res_time
                                break
                
                            else:
                                response = random.choice(intent['responses'])
                                text_to_speech(f"{response}")
                                print(intent['tag'])
                                prev_tag = intent['tag']
                                prev_response = response
                                break
                
                    prev_input = user_input.lower()
                    break
                
                else:
                    for intent in intents['intents']:
                        if intent["tag"] == 'technical':
                            text_to_speech(f"{random.choice(intent['responses'])}")
                            print(intent['tag'])
                            break
                    
while True:
    user_input = input("friday is active: ")

    Friday().Main(user_input)