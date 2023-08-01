import random
import datetime
import json
import torch
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from functions.opinion import opinion
from functions.system_info import info_system

# from functions.is_question import is_question
# from functions.wiki_info import wiki

with open('intents.json', 'r') as json_data:
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
    return datetime.datetime.now().time().strftime('%I:%M %p')

prev_tag = ""
prev_input = ""

while True:
    
    wake_up = input("friday is inactive: ")

    if 'friday' == wake_up.lower():

        while True:
            user_input = input("friday is active: ")
            
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
                        
                        if intent["tag"] == "repeat_string":
                            response = random.choice(intent["responses"])
                            text_to_speech(response.replace("sir", "Mr Stark"))
                            print(intent["tag"])

                        elif intent["tag"] == "system_info":
                            response = random.choice(intent["responses"])
                            text_to_speech(response.replace("{string}", info_system))
                            print(intent["tag"])
                            
                        elif intent['tag'] == 'opinion':
                            text_to_speech(opinion(user_input))
                            prev_tag = intent['tag']
                        
                        elif intent["tag"] == "time":
                            res_time = random.choice(intent['responses']).replace("{time}", get_time())
                            text_to_speech(f"{res_time}")
                            print(intent['tag'])
                            prev_tag = intent['tag']
                        
                        else:
                            text_to_speech(f"{random.choice(intent['responses'])}")
                            print(intent['tag'])
                            prev_tag = intent['tag']

                prev_input = user_input.lower()
                
            else:
                for intent in intents['intents']:
                    if intent["tag"] == 'technical':
                        text_to_speech(f"{random.choice(intent['responses'])}")
                        print(intent['tag'])
                        
    else:
        pass
