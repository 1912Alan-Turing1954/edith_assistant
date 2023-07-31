import os
import nltk
import pickle
import numpy as np
from transformers import pipeline, BertTokenizer, BertForQuestionAnswering
from sklearn.metrics import pairwise_distances_chunked
from sentence_transformers import SentenceTransformer

class QnAModel:
    def __init__(self):
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")
        
        # Specify the cache directory
        self.cache_dir = "preprocessed_content/cache"
        os.makedirs(self.cache_dir, exist_ok=True)

        # Check if cached preprocessed data is available
        self.preprocessed_data = self.load_cached_preprocessed_data()

        if self.preprocessed_data is None:
            # Load the preprocessed content from the .pickle files
            preprocessed_dir = "preprocessed_content"
            preprocessed_files = os.listdir(preprocessed_dir)
            self.preprocessed_data = {}
            for file_name in preprocessed_files:
                if file_name.endswith(".pickle"):
                    topic = file_name.replace("preprocessed_content_", "").replace(".pickle", "")
                    file_path = os.path.join(preprocessed_dir, file_name)
                    content = self.load_preprocessed_content_from_pickle(file_path)
                    if content is not None:
                        self.preprocessed_data[topic] = content

            # Cache the preprocessed data
            self.cache_preprocessed_data()

        # Initialize the BERT-based question-answering model
        tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.question_answering_model = pipeline("question-answering", model=model, tokenizer=tokenizer)

        # Initialize Sentence-BERT model for question and content embeddings
        self.sentence_bert_model = SentenceTransformer("bert-base-nli-mean-tokens")

    def load_preprocessed_content_from_pickle(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = pickle.load(file)
            return content
        except FileNotFoundError:
            return None

    def cache_preprocessed_data(self):
        cache_file_path = os.path.join(self.cache_dir, "cached_preprocessed_data.pickle")
        with open(cache_file_path, "wb") as file:
            pickle.dump(self.preprocessed_data, file)

    def load_cached_preprocessed_data(self):
        cache_file_path = os.path.join(self.cache_dir, "cached_preprocessed_data.pickle")
        try:
            with open(cache_file_path, "rb") as file:
                preprocessed_data = pickle.load(file)
            return preprocessed_data
        except FileNotFoundError:
            return None

    def preprocess_answer(self, answer):
        # Remove special tokens like [CLS], [SEP], etc.
        cleaned_answer = answer.replace('[CLS]', '').replace('[SEP]', '').strip()
        # Clean up any extra spaces around the answer
        cleaned_answer = cleaned_answer.strip()
        # Capitalize the first letter of the answer
        cleaned_answer = cleaned_answer[0].capitalize() + cleaned_answer[1:]
        # Add a period at the end if there's no punctuation
        if not cleaned_answer.endswith(('.', '!', '?')):
            cleaned_answer += '.'
        return cleaned_answer

    def answer_question(self, question, similarity_threshold=0.3):
        # Calculate Sentence-BERT embeddings for the question and preprocessed content
        documents = [question] + list(self.preprocessed_data.values())
        sentence_embeddings = self.sentence_bert_model.encode(documents)

        # Calculate the cosine similarity between the question and content embeddings
        similarity_scores = 1 - np.array(list(pairwise_distances_chunked(sentence_embeddings[0].reshape(1, -1), sentence_embeddings[1:],
                                                        metric='cosine', n_jobs=-1))).flatten()

        # Find the index of the most similar content
        most_similar_index = np.argmax(similarity_scores)

        # Check if the similarity score is above the threshold
        if similarity_scores[most_similar_index] >= similarity_threshold:
            # Get the topic of the most similar content
            topic = list(self.preprocessed_data.keys())[most_similar_index]

            # Get the most similar content
            content = list(self.preprocessed_data.values())[most_similar_index]

            # Use the BERT-based question-answering model with the most similar content
            result = self.question_answering_model(context=content, question=question)

            # Preprocess the answer for better readability
            cleaned_answer = self.preprocess_answer(result['answer'])

            return topic, cleaned_answer
        else:
            return None, None

if __name__ == "__main__":
    qna_model = QnAModel()

    # Ask questions until the user enters "exit"
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        topic, answer = qna_model.answer_question(question)

        if topic and answer:
            print(f"Most Relevant Topic: {topic}")
            print(f"Answer for '{question}' (QA Pipeline): {answer}")
        else:
            print("No relevant answer found.")
