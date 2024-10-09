import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.run_script()

    def initUI(self):
        self.setWindowTitle('Standard Output GUI')
        layout = QVBoxLayout()

        # Text area for displaying output
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def run_script(self):
        print("Running script...")
        try:
            result = subprocess.run(
                ['python', 'scripts/edith/large_language_model/llm_main.py'],

                capture_output=True, text=True, check=True
            )
            print("Script ran successfully.")
            self.output_text.setPlainText(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Script failed.")
            self.output_text.setPlainText(f"Error: {e.stderr}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(400, 300)
    ex.show()
    sys.exit(app.exec_())