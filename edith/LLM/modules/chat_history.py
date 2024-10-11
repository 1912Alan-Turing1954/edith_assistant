import datetime
import json
import logging

class ChatHistory:
    def __init__(self, json_file):
        self.json_file = json_file
        
    def load_chat_history(self) -> list:
        """Load chat history from a JSON file."""
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Error reading dialogue history: {e}. Starting with empty chat history.")
            return []

    def update_chat_history(self, user_input: str, result: str) -> None:
        """Update the chat history with the latest user input and AI response."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        new_entry = {
            "timestamp": timestamp,
            "User": user_input,
            "AI": result
        }

        chat_history = self.load_chat_history()
        chat_history.append(new_entry)

        try:
            with open(self.json_file, 'w') as file:
                json.dump(chat_history, file, indent=4)
            logging.info("Dialogue history updated successfully.")
        except Exception as e:
            logging.error(f"Failed to write to dialogue history: {e}")

    def clear_chat_history(self) -> None:
        """Clear the chat history by writing an empty list to the file."""
        with open(self.json_file, 'w') as file:
            json.dump([], file)
        logging.info("Dialogue history cleared.")
