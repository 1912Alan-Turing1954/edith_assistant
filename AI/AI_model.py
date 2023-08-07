import os
import torch
import PdfReader  # PyMuPDF
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline

# Paths
pdf_directory = "AI/pdfs"
output_directory = "AI/preprocessed_pdfs"
model_name = "bert-large-uncased-whole-word-masking"

# Create output directory if not exists
os.makedirs(output_directory, exist_ok=True)

# Load tokenizer and pre-trained model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Loop through PDF files in the directory
for pdf_filename in os.listdir(pdf_directory):
    if pdf_filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_filename)
        output_filename = os.path.splitext(pdf_filename)[0] + ".txt"
        output_path = os.path.join(output_directory, output_filename)

        # Open PDF
        pdf_document = open(pdf_path, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_document)

        # Extract text from pages
        full_text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            page_text = page.extractText()
            full_text += page_text

        # Close the PDF document
        pdf_document.close()

        # Write extracted text to a text file
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(full_text)

        print(f"Processed {pdf_filename} and saved extracted text to {output_filename}")

# Q&A pipeline
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Examples for training the Q&A model
qa_examples = [
    {
        "question": "What historical event is mentioned in this sentence?",
        "context": sentence,
    }
    for pdf_filename in os.listdir(output_directory)
    if pdf_filename.endswith(".txt")
    for sentence in open(
        os.path.join(output_directory, pdf_filename), "r", encoding="utf-8"
    )
    .read()
    .split(". ")
]

# Fine-tune the model on Q&A examples
for example in qa_examples:
    question = example["question"]
    context = example["context"]
    result = qa_pipeline(question=question, context=context)
    answer = result["answer"]
    print(f"Question: {question}")
    print(f"Context: {context}")
    print(f"Answer: {answer}")
    print("=" * 50)
