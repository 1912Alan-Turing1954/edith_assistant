import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox, QComboBox
)
from PyQt5.QtGui import QColor, QPalette, QFont
from datetime import datetime

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 500)

        self.setup_theme()
        self.setup_ui()
        self.load_tasks()

    def setup_theme(self):
        # Set dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(230, 230, 230))
        palette.setColor(QPalette.Base, QColor(50, 50, 50))
        palette.setColor(QPalette.Text, QColor(230, 230, 230))
        self.setPalette(palette)

        # Set font size and family
        font = QFont("Arial", 11)
        self.setFont(font)

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.task_label = QLabel("Tasks:")
        self.task_label.setStyleSheet("font-size: 18px; font-weight: bold; color: rgb(255, 255, 255);")
        self.layout.addWidget(self.task_label)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: rgb(40, 40, 40); color: rgb(230, 230, 230);")
        self.layout.addWidget(self.task_list)

        # Horizontal layout for task input and priority selection
        input_layout = QHBoxLayout()
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.setStyleSheet("background-color: rgb(60, 60, 60); color: rgb(230, 230, 230); padding: 5px; border-radius: 5px;")
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input)

        # Priority selection
        self.priority_input = QComboBox()
        self.priority_input.setStyleSheet("""
            QComboBox {
                background-color: rgb(60, 60, 60);
                color: rgb(230, 230, 230);
                border: 1px solid rgb(100, 100, 100);
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(50, 50, 50);
                color: rgb(230, 230, 230);
                selection-background-color: rgb(70, 70, 70);
            }
        """)
        self.priority_input.addItems(["Low", "Medium", "High"])
        input_layout.addWidget(self.priority_input)

        self.layout.addLayout(input_layout)

        self.button_layout = QHBoxLayout()
        self.create_buttons()
        self.layout.addLayout(self.button_layout)

        self.task_count_label = QLabel(f"Total Tasks: {self.task_list.count()}")
        self.layout.addWidget(self.task_count_label)

    def create_buttons(self):
        buttons = [
            ("Add Task", self.add_task),
            ("Delete Task", self.delete_task),
            ("Move Up", self.move_task_up),
            ("Move Down", self.move_task_down),
            ("Save Tasks", self.save_tasks),
            ("Load Tasks", self.load_tasks)
        ]

        for label, action in buttons:
            button = QPushButton(label)
            button.clicked.connect(action)
            button.setStyleSheet("""
                background-color: rgb(60, 60, 60);
                color: rgb(230, 230, 230);
                border: none;
                border-radius: 5px;
                padding: 8px;
            """)
            self.button_layout.addWidget(button)

    def update_task_count(self):
        self.task_count_label.setText(f"Total Tasks: {self.task_list.count()}")

    def add_task(self):
        task = self.task_input.text().strip()
        priority = self.priority_input.currentText()
        if task:
            timestamp = datetime.now().strftime("%B %d, %Y - %I:%M %p")
            formatted_task = f"{task}  [Priority: {priority}] [Added: {timestamp}]"
            self.task_list.addItem(formatted_task)
            self.task_input.clear()
            self.update_task_count()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task.")

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")
            return
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))
        self.update_task_count()

    def move_task_up(self):
        current_row = self.task_list.currentRow()
        if current_row > 0:
            item = self.task_list.takeItem(current_row)
            self.task_list.insertItem(current_row - 1, item)
            self.task_list.setCurrentRow(current_row - 1)

    def move_task_down(self):
        current_row = self.task_list.currentRow()
        if current_row < self.task_list.count() - 1:
            item = self.task_list.takeItem(current_row)
            self.task_list.insertItem(current_row + 1, item)
            self.task_list.setCurrentRow(current_row + 1)

    def save_tasks(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)
        QMessageBox.information(self, "Success", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                self.task_list.clear()
                for task in tasks:
                    self.task_list.addItem(task)
                self.update_task_count()
        except (FileNotFoundError, json.JSONDecodeError):
            pass

def task_manager():
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    app.exec_()
