import spacy

def is_question(string):
    # Load the spaCy English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the input string with spaCy
    doc = nlp(string)
    
    # Check if the sentence starts with a question word
    question_words = ['who', 'what', 'when', 'where', 'why', 'how']
    if any(token.text.lower() in question_words for token in doc if token.pos_ == "PRON" or token.pos_ == "ADV"):
        return True

    # Check if the sentence has a question mark at the end
    if doc[-1].text == '?':
        return True

    # Check for question-related sentence structures
    for sent in doc.sents:
        if sent.root.dep_ == 'aux' and sent[-1].text == '?':
            return True

    return False