import json
import sqlite3
import spacy

# Load English language model in SpaCy
nlp = spacy.load('en_core_web_sm')

# Function to analyze user responses using SpaCy
def analyze_user_responses(user_responses):
    likes = []
    dislikes = []
    general_info = {}

    for response in user_responses:
        doc = nlp(response)

        # Extract entities (e.g., names)
        for ent in doc.ents:
            if ent.label_ == 'PERSON' and 'name' not in general_info:
                general_info['name'] = ent.text

        # Extract likes and dislikes based on keywords and noun phrases
        for token in doc:
            if token.lemma_.lower() in ['like', 'enjoy', 'love', 'prefer']:
                likes.extend(extract_noun_phrases(doc[token.i + 1:]))
            elif token.lemma_.lower() in ['dislike', 'hate']:
                dislikes.extend(extract_noun_phrases(doc[token.i + 1:]))

    return likes, dislikes, general_info

# Function to extract noun phrases from SpaCy Doc
def extract_noun_phrases(doc):
    noun_phrases = []
    for chunk in doc.noun_chunks:
        noun_phrases.append(chunk.text)
    return noun_phrases

# Function to generate personality profile from multiple user responses
def generate_personality_profile_from_responses(user_responses):
    # Analyze all user responses
    likes_from_responses, dislikes_from_responses, general_info_from_responses = analyze_user_responses(user_responses)

    # Combine all data into a JSON object
    personality_profile = {
        "name": general_info_from_responses.get('name', ""),
        "likes": list(set(likes_from_responses)),  # Remove duplicates
        "dislikes": list(set(dislikes_from_responses)),  # Remove duplicates
        "general_info": general_info_from_responses
    }

    return personality_profile

def profile_build():
    
    # Initialize SQLite connection
    conn = sqlite3.connect('dialogue_archive.db')
    cursor = conn.cursor()

    # Example query to retrieve user inputs from dialogue table
    cursor.execute('SELECT user_input FROM dialogue')
    rows = cursor.fetchall()

    # Close connection
    conn.close()

    # Extract user inputs from fetched rows
    user_responses = [row[0] for row in rows]

    user_responses
    # Call the function to generate the personality profile
    personality_profile = generate_personality_profile_from_responses(user_responses)

    # Print the personality profile JSON
    print(json.dumps(personality_profile, indent=4))

# print(profile_build())