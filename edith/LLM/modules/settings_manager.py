import json
import logging
import os
from tqdm import tqdm
import time

class SettingsManager:
    def __init__(self, default_timeout=90):
        self.conversation_timeout = default_timeout
        self.protection_password = 'henry'
    
    def settings_menu(self) -> None:
        """Display a sci-fi inspired BIOS settings menu."""
        while True:
            print("\n" + "=" * 70)
            print("           ██████████ BIOS Settings Interface ██████████")
            print("=" * 70)
            print(f" [1] Change Conversation Timeout (Current: {self.conversation_timeout}s)")
            print(f" [2] Change Logging Level (Current: {logging.getLevelName(logging.root.level)})")
            print(f" [3] Set Protection Password (Current: {'Set' if self.protection_password else 'Not Set'})")
            print(" [4] Clear Dialogue History")
            print(" [5] Save current settings to file")
            print(" [6] Exit Settings")
            print("=" * 70)

            choice = input(" Select an option [1-6]: ")

            if choice == "1":
                self.change_conversation_timeout()
            elif choice == "2":
                self.change_logging_level()
            elif choice == "3":
                self.set_protection_password()
            elif choice == "4":
                self.clear_dialogue_history()
            elif choice == "5":
                self.save_settings()
            elif choice == "6":
                logging.info("Exiting settings menu.")
                print(" Exiting settings menu.")
                break
            else:
                logging.warning("Invalid choice in settings menu.")
                print(" ❌ Invalid choice. Please select a valid option.")

    def change_conversation_timeout(self):
        new_timeout = input(" Enter new conversation timeout in seconds: ")
        if new_timeout.isdigit():
            self.conversation_timeout = int(new_timeout)
            logging.info(f"Updated conversation timeout to {self.conversation_timeout}s.")
            with tqdm(total=100, desc="Updating Conversation Timeout") as pbar:
                for _ in range(100):
                    time.sleep(0.01)  # Simulate a delay
                    pbar.update(1)
            print(f" ➤ Updated to {self.conversation_timeout} seconds.")
        else:
            logging.warning("Invalid input for conversation timeout.")
            print(" ❌ Invalid input. Please enter a valid integer.")

    def change_logging_level(self):
        new_logging_level = input(" Enter new logging level (DEBUG, INFO, WARNING, ERROR): ").upper()
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        if new_logging_level in levels:
            logging.getLogger().setLevel(levels[new_logging_level])
            logging.info(f"Updated logging level to {new_logging_level}.")
            with tqdm(total=100, desc="Updating Logging Level") as pbar:
                for _ in range(100):
                    time.sleep(0.01)  # Simulate a delay
                    pbar.update(1)
            print(f" ➤ Updated to {new_logging_level}.")
        else:
            logging.warning("Invalid logging level input.")
            print(" ❌ Invalid logging level.")

    def set_protection_password(self):
        new_password = input(" Enter new protection password: ")
        self.protection_password = new_password
        logging.info("Command password has been set.")
        with tqdm(total=100, desc="Setting Protection Password") as pbar:
            for _ in range(100):
                time.sleep(0.01)  # Simulate a delay
                pbar.update(1)
        print(" ➤ Command password has been set.")

    def save_settings(self):
        settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': logging.getLevelName(logging.root.level),
            'protection': self.protection_password
        }
        try:
            home_dir = os.path.expanduser("~")
    
            # Define the directory path
            settings_dir = os.path.join(home_dir, '.edith_config')
            
            # Create the directory if it doesn't exist
            os.makedirs(settings_dir, exist_ok=True)
            
            # Define the full path for the settings file
            settings_file_path = os.path.join(settings_dir, 'settings.json')
            
            # Save the settings to the file
            with open(settings_file_path, 'w') as f:
                json.dump(settings, f, indent=4)
        
            logging.info("Settings saved successfully to '~/.edith_config/settings.json'.")
            self._simulate_delay("Saving Settings")
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

    def load_settings(self):
        home_dir = os.path.expanduser("~")
    
            # Define the directory path
        settings_dir = os.path.join(home_dir, '.edith_config')
            
        if os.path.exists(settings_dir + 'settings.json'):
            try:
                with open(settings_dir, 'settings.json', 'r') as f:
                    settings = json.load(f)
                self.conversation_timeout = settings.get('conversation_timeout', self.conversation_timeout)
                logging_level = settings.get('logging_level', logging.getLevelName(logging.root.level))
                logging.getLogger().setLevel(logging.getLevelName(logging_level))
                logging.info("Settings loaded successfully from 'settings.json'.")
            except Exception as e:
                logging.error(f"Failed to load settings: {e}")
        else:
            self.create_default_settings()

    def create_default_settings(self):
        default_settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': logging.getLevelName(logging.INFO)
        }
        try:
            home_dir = os.path.expanduser("~")
    
            # Define the directory path
            settings_dir = os.path.join(home_dir, '.edith_config')
            
            # Create the directory if it doesn't exist
            os.makedirs(settings_dir, exist_ok=True)
            
            # Save the set
            with open(settings_dir + "/settings.json", 'w') as f:
                json.dump(default_settings, f, indent=4)
            logging.info("Default settings created successfully in 'settings.json'.")
        except Exception as e:
            logging.error(f"Failed to create default settings: {e}")

    def _simulate_delay(self, message):
        with tqdm(total=100, desc=message) as pbar:
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)
