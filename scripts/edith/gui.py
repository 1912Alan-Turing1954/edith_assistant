import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edith")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create a text area for output
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        # Run the script and display output
        self.run_script()

    def run_script(self):
        try:
            # Replace with the path to your script
            result = subprocess.run(['python', 'scripts/edith/large_language_model/llm_main.py'], capture_output=True, text=True)
            self.text_area.append(result.stdout + result.stderr)
        except Exception as e:
            self.text_area.append(f"Error running script: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SimpleApp()
    main_window.show()
    sys.exit(app.exec_())
