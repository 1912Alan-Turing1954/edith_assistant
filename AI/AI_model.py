import json
import os
import joblib
import nltk
import torch
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import load_dataset
import tqdm


# Preprocess the dataset
def preprocess_data(dataset):
    preprocessed_data = []
    for question, answer in dataset:
        question_tokens = word_tokenize(question.lower())
        answer_tokens = word_tokenize(answer.lower())
        preprocessed_data.append((question_tokens, answer_tokens))
    return preprocessed_data


# Train the Q&A model incrementally
def incremental_train_qna_model(dataset, model_data=None):
    if model_data is None:
        # If no model_data is provided, initialize a new model
        model_data = {
            "tfidf_vectorizer": TfidfVectorizer(
                tokenizer=lambda x: x, preprocessor=lambda x: x
            ),
            "preprocessed_data": [],
        }

    # Preprocess the new dataset
    new_preprocessed_data = preprocess_data(dataset)
    model_data["preprocessed_data"].extend(new_preprocessed_data)

    # Train the model on the updated dataset
    questions = [
        question_tokens for question_tokens, _ in model_data["preprocessed_data"]
    ]
    model_data["tfidf_vectorizer"].fit(questions)

    return model_data


# Perform inference on the trained model
def predict_answer(model_data, query):
    tfidf_vectorizer = model_data["tfidf_vectorizer"]
    preprocessed_data = model_data["preprocessed_data"]

    query_tokens = word_tokenize(query.lower())
    query_vector = tfidf_vectorizer.transform([query_tokens])

    similarities = cosine_similarity(
        query_vector, tfidf_vectorizer.transform([q for q, _ in preprocessed_data])
    )
    most_similar_idx = similarities.argmax()

    _, answer_tokens = preprocessed_data[most_similar_idx]
    return " ".join(answer_tokens)


if __name__ == "__main__":
    # Load the latest model and data checkpoint from the previous run (if available)
    model_checkpoint_file = os.path.join(
        os.getcwd(), "model/qa_model_checkpoint.joblib"
    )
    if os.path.exists(model_checkpoint_file):
        model_data = joblib.load(model_checkpoint_file)
    else:
        model_data = None

    # Incremental training
    num_iterations = 3  # Set the number of iterations you want to perform
    dataset_split_percentage = (
        1  # Load approximately 1% of the dataset in each iteration
    )

    # Check if GPU is available and set the device accordingly
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print(f"Using device: {device}")

    for i in range(num_iterations):
        # Load the Wikipedia dataset for the current iteration with the specified percentage split
        dataset = load_dataset(
            "wikipedia", "20220301.en", split=f"train[:{dataset_split_percentage}%]"
        )

        # Get the actual data (text column) from the loaded dataset
        data = dataset["text"]

        # Convert the text data into question-answer pairs
        question_answer_pairs = [
            (data[i], data[i + 1]) for i in range(0, len(data) - 1, 2)
        ]

        # Incremental training for this iteration
        model_data = incremental_train_qna_model(
            question_answer_pairs, model_data=model_data
        )

        # Save the updated model and data checkpoint for future use
        if not os.path.exists(model_checkpoint_file):
            joblib.dump(model_data, model_checkpoint_file)

        # Display the progress bar for each iteration
        progress = (i + 1) / num_iterations * 100
        tqdm.write(f"Iteration {i + 1}/{num_iterations} - Progress: {progress:.2f}%")

    # At the end of all iterations, save the final model checkpoint
    joblib.dump(model_data, model_checkpoint_file)
