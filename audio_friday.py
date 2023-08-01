import random
import datetime
import json
import torch
import speech_recognition as sr  # Import the speech_recognition library
from brain.model import NeuralNet
from brain.nltk_utils import bag_of_words, tokenize
from tts_.tts import text_to_speech
from functions.opinion import opinion
from functions.is_question import is_question
from functions.wiki_info import wiki
from functions.system_info import info_system
# import pywhatkit

# pywhatkit.playonyt('Claire de lune')

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

# Initialize the recognizer
recognizer = sr.Recognizer()

def is_wake_word(phrase):
    return "friday" in phrase.lower()

def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            phrase = recognizer.recognize_google(audio).lower()
            if is_wake_word(phrase):
                print("Wake word detected!")
                return
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Error occurred while requesting results from Google Speech Recognition service: {e}")

def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You said:", user_input)

            # Rest of your code remains unchanged
            # ... (Your existing code from here) ...
        
            if user_input == prev_input:
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
                        
            # Once processing is done, break out of the listening loop
            break

        except sr.UnknownValueError:
            print("Sorry, I could not understand you.")
        except sr.RequestError as e:
            print(f"Error occurred while requesting results from Google Speech Recognition service: {e}")

# Main loop
while True:
    listen_for_wake_word()  # Wait for the wake word "friday" to activate listening
    while True:
        listen()  # Enter active listening mode and process user input
