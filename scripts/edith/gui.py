import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class ScriptRunner(QThread):
    output_ready = pyqtSignal(str)

    def run(self):
        try:
            print("Starting subprocess...", flush=True)  # Debugging output
            result = subprocess.run(
                [sys.executable, 'edith/large_language_model/llm_main.py'],
                capture_output=True, text=True, timeout=10  # Timeout after 10 seconds
            )

            print("Subprocess completed.", flush=True)  # Debugging output
            if result.returncode != 0:
                self.output_ready.emit(f"Error: {result.stderr}")
            else:
                self.output_ready.emit(result.stdout)
        except Exception as e:
            self.output_ready.emit(f"Error running script: {e}")

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.run_script()

    def setup_ui(self):
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

    def run_script(self):
        self.text_area.append("Running script...")
        self.thread = ScriptRunner()
        self.thread.output_ready.connect(self.display_output)
        self.thread.start()

    def display_output(self, output):
        self.text_area.append(output)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = SimpleApp()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}", flush=True)
