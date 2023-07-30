import nltk
import pickle
import os
from transformers import pipeline

def load_preprocessed_content_from_pickle(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
        return content
    except FileNotFoundError:
        return None

def main():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")

    # Specify the directory path containing the preprocessed pickle files
    preprocessed_dir = "preprocessed_content"

    # Load all preprocessed content from pickle files
    preprocessed_content = {}
    dictionary_content = None  # To store the dictionary content separately
    for file_name in os.listdir(preprocessed_dir):
        if file_name.endswith(".pickle"):
            page_title = file_name.replace("preprocessed_content_", "").replace(".pickle", "")
            if page_title.lower() == "oxford-english-dictionary":
                # Load the dictionary content separately
                preprocessed_pickle_file_path = os.path.join(preprocessed_dir, file_name)
                dictionary_content = load_preprocessed_content_from_pickle(preprocessed_pickle_file_path)
            else:
                preprocessed_pickle_file_path = os.path.join(preprocessed_dir, file_name)
                content = load_preprocessed_content_from_pickle(preprocessed_pickle_file_path)
                if content is not None:
                    preprocessed_content[page_title] = content

    if not preprocessed_content:
        print("No preprocessed content found. Please run 'preprocess_wikipedia.py' first.")
        return

    print("Preprocessed content loaded from the .pickle files.")

    # Ask questions until the user enters "exit"
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        # Use the question-answering pipeline with a larger model
        question_answering_model = pipeline("question-answering", model="bert-large-cased-whole-word-masking-finetuned-squad")

        if question.lower().startswith("define"):
            # Handle "define" queries using the dictionary content
            if dictionary_content is not None:
                result = question_answering_model(context=dictionary_content, question=question)
                print(f"Answer from Dictionary (QA Pipeline): {result['answer']}")
            else:
                print("Dictionary content not found. Please preprocess and save the dictionary first.")
        else:
            # Handle other queries using the loaded preprocessed content
            for page_title, content in preprocessed_content.items():
                result = question_answering_model(context=content, question=question)
                print(f"Answer for '{page_title}' (QA Pipeline): {result['answer']}")

if __name__ == "__main__":
    main()
