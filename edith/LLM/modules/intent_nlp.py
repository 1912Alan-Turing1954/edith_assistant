import json
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from collections import Counter
import logging
from typing import Tuple, List

# Setup logging
logging.basicConfig(level=logging.INFO)

document_analysis_response = [
    "Will do, sir. Document analysis is underway.",
    "On it! Commencing document analysis now.",
    "Got it! Analyzing the document as you requested.",
    "Reviewing the document for valuable insights.",
    "Examining the document for key points.",
    "Will do! Summarizing the document for you.",
    "The document is currently being processed for analysis.",
    "Sure thing! Running a detailed analysis on the document."
    "yes, boss",
    "yes, sir",
    "on it",
    "will do",
    'will do sir'
]

data_visualization_response = [
    "Will do, sir. Starting data visualization now.",
    "On it! Data visualization is in progress.",
    "Got it! Visualizing the data right away.",
    "Creating data visuals for you.",
    "Analyzing insights from the data.",
    "Will do! Generating the visualizations now.",
    "Processing data for visualization, please hold on.",
    "Absolutely! Running the data visualization."
    "yes, boss",
    "yes, sir",
    "on it",
    "will do",
    'will do sir'
]

task_manager_response = [
    "Will do, sir. Starting task manager.",
    "On it! Task manager active.",
    "Absolutely! Opening task manager.",
    "Got it! Initializing task management.",
    "On it! Activating task manager.",
    "Will do! Task management underway.",
    "Launching task manager, sir.",
    "Task manager ready to go!"
    "yes, boss",
    "yes, sir",
    "on it",
    "will do",
    'will do sir'
]

map_response = [
    "Will do, sir. Opening map.",
    "On it! Map is now active.",
    "Got it! Initializing map display.",
    "On it! Activating world map.",
    "Launching world map, sir.",
    "Map is ready to go!",
    "yes, boss",
    "yes, sir",
    "on it",
    "will do",
    'will do sir'
]


def load_intents(file_path: str) -> dict:
    """Load intents from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from the intents file.")
        raise

# Download necessary NLTK resources (only need to run once)
nltk.download('punkt')

def bag_of_words(tokenized_sentence: List[str], all_words: List[str]) -> np.ndarray:
    """Create a bag of words array."""
    bag = [0] * len(all_words)  # Initialize bag of words array
    word_counts = Counter(tokenized_sentence)
    
    for i, word in enumerate(all_words):
        bag[i] = word_counts[word]  # Fill the bag with counts
    
    return np.array(bag)

def classify_input(user_input: str, intents: dict, confidence_threshold: float) -> Tuple[str, float, bool, str]:
    """Classify user input and return a response with confidence score."""
    tokens = word_tokenize(user_input.lower())  # Tokenize and lowercase the input
    
    all_words = []
    tags = []
    
    for intent in intents["intents"]:
        tag = intent["tag"]
        tags.append(tag)
        for pattern in intent["patterns"]:
            all_words.extend(pattern.split())
    
    all_words = sorted(set(all_words))
    
    bag = bag_of_words(tokens, all_words)
    
    # Calculate scores for each intent based on bag of words
    scores = []
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_bag = bag_of_words(pattern.split(), all_words)
            similarity = np.dot(bag, pattern_bag) / (np.linalg.norm(bag) * np.linalg.norm(pattern_bag) + 1e-10)  # Cosine similarity
            scores.append((similarity, intent))

    # Sort scores by similarity
    scores = sorted(scores, key=lambda x: x[0], reverse=True)
    
    # Get the best score
    best_score, best_intent = scores[0]

    if best_score > confidence_threshold:
        intent_tag = best_intent['tag']
        
        # Select response based on the intent
        response_1 = np.random.choice(best_intent["responses"])  # General response from the intent's response list
        if intent_tag == "ghost_net_protocol":
            if "disable" in user_input or "deactivate" in user_input:
                response_2 = np.random.choice(document_analysis_response)  # Random choice from document_analysis_response
            else:
                response_2 = np.random.choice(data_visualization_response)  # Random choice from data_visualization_response
        elif intent_tag == "document_analysis":
            response_2 = np.random.choice(document_analysis_response)  # Random choice from document_analysis_response
        elif intent_tag == "commence_data_visualization":
            response_2 = np.random.choice(data_visualization_response)  # Random choice from data_visualization_response
        elif intent_tag == "start_task_manager":
            response_2 = np.random.choice(task_manager_response)  # Random choice from task_manager_response
        elif intent_tag == "open_map":
            response_2 = np.random.choice(map_response)  # Random choice from map_response
        else:
            response_2 = "I'm not sure how to respond to that."
        
        result = True  # Intent recognized
    else:
        response_1 = "I didn't understand that. Do you mind repeating that?"
        response_2 = ""
        result = False  # Intent not recognized

    return response_1, best_score, result, response_2

def classify_intent(user_input: str) -> None:
    """Main function to run the command interface."""
    logging.info("Starting Command Interface...")
    
    intents_file = "edith/models/intent_model/intents.json"
    confidence_threshold = 0.8  # Adjustable threshold
    
    intents = load_intents(intents_file)
        
    response_1, confidence, result, response_2 = classify_input(user_input, intents, confidence_threshold)
    logging.info(f"User Input: {user_input} | Response 1: {response_1} | Response 2: {response_2} | Confidence: {confidence:.2f} | Result: {result}")
    return response_1, response_2, result

# # Example usageremove
# print(classify_intent('perform document analysis'))
