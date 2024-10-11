import json
import logging
import os
import tqdm
import time

class SettingsManager:
    def __init__(self, default_timeout=90):
        self.conversation_timeout = default_timeout
        self.protection_password = 'henry'
    
    def save_settings(self):
        settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': logging.getLevelName(logging.root.level),
            'protection': self.protection_password
        }
        try:
            with open('docs/settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            logging.info("Settings saved successfully to 'settings.json'.")
            self._simulate_delay("Saving Settings")
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

    def load_settings(self):
        if os.path.exists('docs/settings.json'):
            try:
                with open('docs/settings.json', 'r') as f:
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
            with open('docs/settings.json', 'w') as f:
                json.dump(default_settings, f, indent=4)
            logging.info("Default settings created successfully in 'settings.json'.")
        except Exception as e:
            logging.error(f"Failed to create default settings: {e}")

    def _simulate_delay(self, message):
        with tqdm(total=100, desc=message) as pbar:
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)
