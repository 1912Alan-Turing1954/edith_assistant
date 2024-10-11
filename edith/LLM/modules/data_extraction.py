import os
import PyPDF2
from PyPDF2 import PdfReader
from docx import Document
from PyQt5 import QtWidgets, QtCore
import pytesseract
from PIL import Image

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

def extract_text_from_image(image_path):

    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def extract_text_from_other_formats(file_path):
    # You can handle other formats here or raise an error
    raise NotImplementedError(f"Extraction for format not supported: {file_path}")

def make_readable(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    else:
        try:
            return extract_text_from_other_formats(file_path)
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""

class TextExtractorApp(QtWidgets.QWidget):
    text_extracted = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Document Text Extractor')
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Enter the path for the document or click to find it:')
        layout.addWidget(self.label)

        self.path_entry = QtWidgets.QLineEdit(self)
        layout.addWidget(self.path_entry)

        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.extract_button = QtWidgets.QPushButton('Extract Text', self)
        self.extract_button.clicked.connect(self.extract_text)
        layout.addWidget(self.extract_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background-color: #2E2E2E; color: #FFFFFF; }
            QLineEdit { background-color: #3E3E3E; color: #FFFFFF; border: 1px solid #555555; }
            QPushButton { background-color: #3E3E3E; color: #FFFFFF; border: 1px solid #555555; padding: 5px; }
            QPushButton:hover { background-color: #4E4E4E; }
            QLabel { font-size: 14px; }
        """)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a Document", "", 
            "All Files (*.*);;PDF Files (*.pdf);;Word Files (*.docx);;Text Files (*.txt);;Image Files (*.jpg *.jpeg *.png)")
        if file_path:
            self.path_entry.setText(file_path)

    def extract_text(self):
        file_path = self.path_entry.text().strip()
        if os.path.isfile(file_path):
            text = make_readable(file_path)
            if text:
                self.text_extracted.emit(text)
                self.close()
            else:
                print("No text extracted.")
        else:
            print("Invalid file.")

def extract_file_contents():
    app = QtWidgets.QApplication([])
    window = TextExtractorApp()
    window.resize(600, 200)

    extracted_text = []
    window.text_extracted.connect(lambda text: extracted_text.append(text))

    window.show()
    app.exec_()
    
    return extracted_text[0] if extracted_text else None
