import json
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from collections import Counter
import logging
from typing import Tuple, List

# Setup logging
logging.basicConfig(level=logging.INFO)

off_response = [
    "The Ghost Net Protocol has been disabled.",
    "The Ghost Net Protocol is currently deactivated.",
    "The Ghost Net Protocol has been stopped.",
    "The Ghost Net Protocol override has been initiated.",
    "Ghost Net Protocol has been successfully turned off.",
    "Ghost Net Protocol is now inactive.",
    "Deactivating Ghost Net Protocol. Please hold on...",
    "Ghost Net Protocol has been halted."
]

on_response = [
    "The Ghost Net Protocol has been activated.",
    "The Ghost Net Protocol is now enabled.",
    "The Ghost Net Protocol is starting.",
    "The Ghost Net Protocol is restarting.",
    "Ghost Net Protocol has been successfully turned on.",
    "Ghost Net Protocol is now fully operational.",
    "Activating Ghost Net Protocol. Please wait...",
    "Ghost Net Protocol is up and running."
]

document_analysis_response = [
    "Document analysis is now being performed.",
    "The document analysis has commenced.",
    "I am analyzing the document as requested.",
    "Reviewing the document for insights.",
    "Examining the document for key points.",
    "Summarizing the document for you.",
    "The document is being processed for analysis.",
    "I am running a detailed analysis on the document."
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

def classify_input(user_input: str, intents: dict, confidence_threshold: float) -> Tuple[str, float]:
    """Classify user input and return a response with confidence score."""
    tokens = word_tokenize(user_input)
    
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
        result = True
        return np.random.choice(best_intent["responses"]), best_score, result
    else:
        result = False
        return "I didn't understand that. Do you mind repeating that?", 0.0, result

def classify_intent(user_input: str) -> None:
    """Main function to run the command interface."""
    logging.info("Starting Command Interface...")
    
    intents_file = "edith/models/intent_model/intents.json"
    confidence_threshold = 0.1  # Adjustable threshold
    
    intents = load_intents(intents_file)
        
    response, confidence, result = classify_input(user_input, intents, confidence_threshold)
    logging.info(f"User Input: {user_input} | Response: {response} | Confidence: {confidence:.2f}")
    return response, result


