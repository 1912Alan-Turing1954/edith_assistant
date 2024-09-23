import os
import textract
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_text_from_other_formats(file_path):
    return textract.process(file_path).decode('utf-8').strip()

def make_readable(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        try:
            return extract_text_from_other_formats(file_path)
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""

def list_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Error accessing directory: {e}")
        return []

def extract_data():
    # Prompt for the directory
    directory = input("Enter the directory path to search for documents: ").strip()
    
    if os.path.isdir(directory):
        files = list_files_in_directory(directory)
        print("Files in directory:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file}")
        
        # Prompt for file selection
        file_index = int(input("Enter the number of the file you want to select: ")) - 1
        
        if 0 <= file_index < len(files):
            selected_file = os.path.join(directory, files[file_index])
            text = make_readable(selected_file)
            if text:
                print("Extracted Text:")
                print(text)
            else:
                print("No text extracted.")
        else:
            print("Invalid selection.")
    else:
        print("Invalid directory.")

