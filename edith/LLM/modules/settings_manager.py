import sys
import json
import logging
import os
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, 
                             QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QComboBox)

class SettingsManager:
    def __init__(self, default_timeout=30):
        self.conversation_timeout = default_timeout
        self.protection_password = 'henry'
        self.logging_level = logging.getLevelName(logging.root.level)

    def save_settings(self):
        settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': self.logging_level,
            'protection': self.protection_password
        }
        try:
            home_dir = os.path.expanduser("~")
            settings_dir = os.path.join(home_dir, '.edith_config')
            os.makedirs(settings_dir, exist_ok=True)
            settings_file_path = os.path.join(settings_dir, 'settings.json')
            with open(settings_file_path, 'w') as f:
                json.dump(settings, f, indent=4)
            logging.info("Settings saved successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")
            return False

    def load_settings(self):
        home_dir = os.path.expanduser("~")
        settings_dir = os.path.join(home_dir, '.edith_config')
        settings_file_path = os.path.join(settings_dir, 'settings.json')
        
        if os.path.exists(settings_file_path):
            try:
                with open(settings_file_path, 'r') as f:
                    settings = json.load(f)
                self.conversation_timeout = settings.get('conversation_timeout', self.conversation_timeout)
                self.logging_level = settings.get('logging_level', logging.getLevelName(logging.root.level))
                self.protection_password = settings.get('protection', self.protection_password)
                logging.info("Settings loaded successfully.")
            except Exception as e:
                logging.error(f"Failed to load settings: {e}")

class SettingsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('BIOS Settings Interface')
        self.setGeometry(100, 100, 400, 300)

        # Set dark style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E; /* Dark background */
            }
            QLabel {
                color: #FFFFFF; /* White text */
            }
            QLineEdit {
                background-color: #4A4A4A; /* Dark input background */
                color: #FFFFFF; /* White text */
                border: 1px solid #AAAAAA; /* Light border */
            }
            QComboBox {
                background-color: #4A4A4A; /* Dark combo box background */
                color: #FFFFFF; /* White text */
                border: 1px solid #AAAAAA; /* Light border */
            }
            QPushButton {
                background-color: #5A5A5A; /* Dark button background */
                color: #FFFFFF; /* White text */
                border: 1px solid #AAAAAA; /* Light border */
            }
            QPushButton:hover {
                background-color: #6A6A6A; /* Lighter button on hover */
            }
        """)

        layout = QVBoxLayout()

        # Conversation Timeout
        self.timeout_label = QLabel(f'Conversation Timeout (Current: {self.settings_manager.conversation_timeout}s)')
        layout.addWidget(self.timeout_label)
        self.timeout_input = QLineEdit()
        layout.addWidget(self.timeout_input)

        # Logging Level
        self.logging_label = QLabel(f'Logging Level (Current: {self.settings_manager.logging_level})')
        layout.addWidget(self.logging_label)
        self.logging_combo = QComboBox()
        self.logging_combo.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR'])
        layout.addWidget(self.logging_combo)

        # Protection Password
        self.password_label = QLabel('Protection Password:')
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        layout.addWidget(self.password_input)

        # Buttons
        self.save_button = QPushButton('Save Settings')
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton('Load Settings')
        self.load_button.clicked.connect(self.load_settings)
        layout.addWidget(self.load_button)

        self.clear_button = QPushButton('Clear Dialogue History (not implemented)')
        layout.addWidget(self.clear_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_settings(self):
        self.settings_manager.load_settings()
        self.timeout_label.setText(f'Conversation Timeout (Current: {self.settings_manager.conversation_timeout}s)')
        self.logging_label.setText(f'Logging Level (Current: {self.settings_manager.logging_level})')
        self.password_input.setText(self.settings_manager.protection_password)

    def save_settings(self):
        try:
            new_timeout = int(self.timeout_input.text())
            self.settings_manager.conversation_timeout = new_timeout
            self.settings_manager.logging_level = self.logging_combo.currentText()
            self.settings_manager.protection_password = self.password_input.text()

            if self.settings_manager.save_settings():
                QMessageBox.information(self, 'Success', 'Settings saved successfully.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to save settings.')
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid integer for timeout.')

def settings_gui():
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.INFO)
    window = SettingsGUI()
    window.show()
    app.exec_()  # This will not terminate the script
