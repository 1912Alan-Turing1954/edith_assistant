import nltk
import pickle
import os
import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import fitz

def fetch_wikipedia_page(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles={page_title}"
    response = requests.get(url)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    if 'extract' in page:
        return page['extract']
    else:
        return None

def preprocess_text(text):
    # Clean HTML tags and formatting
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()

    # Remove special characters, numbers, and punctuation
    cleaned_text = re.sub(r"[^a-zA-Z]", " ", cleaned_text)

    # Convert to lowercase and tokenize
    tokens = word_tokenize(cleaned_text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens into a single string with proper spacing
    preprocessed_text = " ".join(lemmatized_tokens)

    # Clean up any extra spaces between words
    preprocessed_text = re.sub(r'\s+', ' ', preprocessed_text).strip()

    return preprocessed_text

def save_preprocessed_content_to_pickle(file_path, content):
    with open(file_path, 'wb') as file:
        pickle.dump(content, file)

def extract_text_from_pdf(pdf_file_path):
    pdf_text = ""
    with fitz.open(pdf_file_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pdf_text += page.get_text()
    return pdf_text

def main():
    # Specify the directory path to save the preprocessed content
    save_dir = "preprocessed_content"
    os.makedirs(save_dir, exist_ok=True)

    # List of page titles and PDF file paths to fetch or read from
    page_titles_and_pdfs = [
        "Python_(programming_language)",
        "Artificial_intelligence",
        "Machine_learning",
        "History",
        "Mathematics",
        "Science",
        "Physics",
        "Middle Ages",
        "Vikings",
        "Dark Ages (historiography)"
        # Add your PDF file path here
        # Add more page titles and PDF file paths here
    ]

    for item in page_titles_and_pdfs:
        if item.endswith(".pdf"):
            pdf_file_path = item
            pdf_content = extract_text_from_pdf(pdf_file_path)

            if pdf_content:
                print(f"Original PDF Content for '{pdf_file_path}':")
                print(pdf_content)

                preprocessed_content = preprocess_text(pdf_content)
                print(f"\nPreprocessed PDF Content for '{pdf_file_path}':")
                print(preprocessed_content)

                # Save the preprocessed content to a .pickle file in the specified directory
                file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
                preprocessed_pickle_file_path = os.path.join(save_dir, f"preprocessed_content_{file_name}.pickle")
                save_preprocessed_content_to_pickle(preprocessed_pickle_file_path, preprocessed_content)
                print(f"\nPreprocessed content saved to '{preprocessed_pickle_file_path}'.")
            else:
                print(f"Failed to extract text from PDF '{pdf_file_path}'.")
        else:
            page_title = item
            wikipedia_content = fetch_wikipedia_page(page_title)

            if wikipedia_content:
                print(f"Original Wikipedia Content for '{page_title}':")
                print(wikipedia_content)

                preprocessed_content = preprocess_text(wikipedia_content)
                print(f"\nPreprocessed Wikipedia Content for '{page_title}':")
                print(preprocessed_content)

                # Save the preprocessed content to a .pickle file in the specified directory
                preprocessed_pickle_file_path = os.path.join(save_dir, f"preprocessed_content_{page_title}.pickle")
                save_preprocessed_content_to_pickle(preprocessed_pickle_file_path, preprocessed_content)
                print(f"\nPreprocessed content saved to '{preprocessed_pickle_file_path}'.")
            else:
                print(f"Failed to fetch the Wikipedia page for '{page_title}'.")

if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    main()
