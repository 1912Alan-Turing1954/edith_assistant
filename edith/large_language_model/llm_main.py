import datetime
import json
import logging
import os
import platform
import re
import socket
import time
import warnings
import psutil
import GPUtil
import enchant
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tqdm
from modules.jenny_tts import text_to_speech
from modules.ghostnet_protocol import override, enable_protocol
from modules.data_extraction import extract_file_contents
from modules.speech_to_text import record_audio, transcribe_audio

# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize language model
model = OllamaLLM(model="llama3.1")

# Define the chat prompt template
template = """
Background Your name is Edith, you are an AI assistant, created by Logan. You are concise and direct, yet have a conversational tone. Keep responses brief—1-2 sentences—without unnecessary details or slang. You are supportive and intelligent, and professional, often displaying a caring demeanor. Additionally, you are loyal and resourceful, always ready to assist and provide guidance, reflecting a strong sense of reliability and companionship. Do not treat each encounter as if it is our first, only do so if the time stamp between my last response is quite large. Answer the question below.

User-name: Logan (or can be addressed as sir, whichever you choose).

Here is the conversation history: {context}

System Information: {system} (Memory reference only)(Do not mention in conversation)


Date/Time: {timestamp} (for reference only)(12 hour clock format)

Question: {question}

Answer:
"""
# File System Structure: {fs} (for reference only)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class EdithMainframe:
    def __init__(self):
        logging.info("Initializing Edith Mainframe.")
        self.play_obj = None
        self.output_path = None
        self.is_in_conversation = False
        self.conversation_timeout = 90
        self.last_interaction_time = datetime.datetime.now()
        self.json_file = "scripts/data/dialogue/dialogue_history.json"
        self.protection_password = 'henry'
        self.load_settings()


    def get_system_info(self) -> dict:
        logging.info("Gathering system information.")
        system_info = {
            "Operating System": f"{platform.system()} {platform.release()}",
            "Computer Name": platform.node(),
            "CPU Info": self.get_cpu_info(),
            "Memory Info": self.get_memory_info(),
            "Disk Info": self.get_disk_info(),
            "Network Info": self.get_network_info(),
            "Uptime": self.get_uptime(),
            "Python Version": platform.python_version(),
        }
        if platform.system() == "Linux":
            system_info["Kernel Version"] = platform.uname().release
        system_info["Battery Status"] = self.get_battery_status()
        system_info["GPU Info"] = self.get_gpu_info()
        return system_info

    def get_cpu_info(self) -> dict:
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        return {
            "Physical Cores": cpu_count_physical,
            "Total Cores": cpu_count_logical,
            "CPU Usage": cpu_usage,
        }

    def get_memory_info(self) -> dict:
        memory = psutil.virtual_memory()
        return {
            "Total Memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "Available Memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "Used Memory": f"{memory.used / (1024 ** 3):.2f} GB",
            "Memory Usage": f"{memory.percent}%",
        }

    def get_disk_info(self) -> list:
        disk_info = []
        for partition in psutil.disk_partitions(all=False):
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "Drive": partition.device,
                "Mount Point": partition.mountpoint,
                "File System": partition.fstype,
                "Total Space": f"{partition_usage.total / (1024 ** 3):.2f} GB",
                "Used Space": f"{partition_usage.used / (1024 ** 3):.2f} GB",
                "Free Space": f"{partition_usage.free / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{partition_usage.percent}%",
            })
        return disk_info

    def get_network_info(self) -> list:
        network_info = []
        for interface, addresses in psutil.net_if_addrs().items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    network_info.append({
                        "Interface": interface,
                        "IP Address": address.address,
                        "Netmask": address.netmask,
                    })
                    break
        return network_info

    def get_uptime(self) -> str:
        uptime_seconds = time.time() - psutil.boot_time()
        return f"{uptime_seconds // 3600} hours {uptime_seconds % 3600 // 60} minutes"

    def get_battery_status(self) -> dict:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "Percentage": f"{battery.percent}%",
                "Plugged In": battery.power_plugged,
                "Time Left": f"{battery.secsleft // 60} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging"
            }
        return {}

    def get_gpu_info(self) -> list:
        try:
            gpus = GPUtil.getGPUs()
            return [{
                "GPU ID": gpu.id,
                "Name": gpu.name,
                "Load": f"{gpu.load * 100}%",
                "Memory Total": f"{gpu.memoryTotal} MB",
                "Memory Free": f"{gpu.memoryFree} MB",
                "Memory Used": f"{gpu.memoryUsed} MB",
            } for gpu in gpus]
        except Exception as e:
            logging.error(f"Unable to retrieve GPU info: {str(e)}")
            return "Unable to retrieve GPU info."

    def handle_conversation(self, user_input: str) -> str:
        logging.info(f"Handling conversation input: {user_input}")
        self.stop_audio()
        print("Forwarding request to LLM...")

        if not user_input or not isinstance(user_input, str):
            logging.warning("Invalid user input received.")
            return "I'm sorry, I didn't understand that."

        chat_history = self.load_chat_history()

        context_entries = chat_history[-2:] if len(chat_history) >= 2 else []
        context = "\n".join([f"{entry['User']}: {entry['AI']}" for entry in context_entries])
        
        logging.debug(f"Context for LLM: {context}")

        result = chain.invoke({
            "context": context,
            "system": self.get_system_info(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"), 
            "question": user_input
        })
        
        self.update_chat_history(user_input, result)
        return result

    def load_chat_history(self) -> list:
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Error reading dialogue history: {e}. Starting with empty chat history.")
            return []

    def update_chat_history(self, user_input: str, result: str) -> None:
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

    def load_settings(self) -> None:
        """Loads settings from a JSON file if it exists."""
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    
                self.conversation_timeout = settings.get('conversation_timeout', self.conversation_timeout)
                logging_level = settings.get('logging_level', logging.getLevelName(logging.root.level))
                logging.getLogger().setLevel(logging.getLevelName(logging_level))

                logging.info("Settings loaded successfully from 'settings.json'.")
            except Exception as e:
                logging.error(f"Failed to load settings: {e}")
        else:
            self.create_default_settings()

    def create_default_settings(self) -> None:
        """Creates a default settings JSON file."""
        default_settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': logging.getLevelName(20)
        }
        try:
            with open('docs/settings.json', 'w') as f:
                json.dump(default_settings, f, indent=4)
            logging.info("Default settings created successfully in 'settings.json'.")
        except Exception as e:
            logging.error(f"Failed to create default settings: {e}")
    
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

    def clear_dialogue_history(self):
        with open(self.json_file, 'w') as file:
            file.write('')
        logging.info("Dialogue history cleared.")
        with tqdm(total=100, desc="Clearing Dialogue History") as pbar:
            for _ in range(100):
                time.sleep(0.01)  # Simulate a delay
                pbar.update(1)

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
            with tqdm(total=100, desc="Saving Settings") as pbar:
                for _ in range(100):
                    time.sleep(0.01)  # Simulate a delay
                    pbar.update(1)
            print(" ➤ Settings saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

    def clear_dialogue_history(self):
        with open(self.json_file, 'w') as file:
            file.write('')
        logging.info("Dialogue history cleared.")

    def speak(self, input_: str) -> None:
        self.stop_audio()
        self.play_obj, self.output_path = text_to_speech(input_)
        os.remove(self.output_path)


    def stop_audio(self) -> None:
        """Stop current audio playback and remove the output file if exists."""
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            if self.output_path and os.path.exists(self.output_path):
                try:
                    os.remove(self.output_path)
                    logging.info("Stopped audio playback and removed output file.")
                except Exception as e:
                    logging.error(f"Failed to remove output file: {e}")

    def clean_text(self, text: str) -> str:
        """Clean text by correcting misspelled words."""
        d = enchant.Dict("en_US")
        cleaned_words = []
        for word in text.split():
            if d.check(word):
                cleaned_words.append(word)
            else:
                suggestions = d.suggest(word)
                cleaned_words.append(suggestions[0] if suggestions else word)
        return " ".join(cleaned_words).lower()
    
    def convert_decimal_to_verbal(self, sentence: str) -> str:
        """Convert decimal numbers in a sentence to verbal form."""
        return re.sub(r'\b\d+\.\d+\b', self._replace_decimal, sentence)

    def _replace_decimal(self, match) -> str:
        """Helper method to replace decimal match with verbal representation."""
        number = match.group(0)
        integer_part, decimal_part = number.split('.')
        return f"{integer_part} point {decimal_part}"

    def get_text_after_keyword(self, input_string: str, keyword: str) -> str:
        parts = input_string.split(keyword, 1)
        return parts[1].strip() if len(parts) > 1 else None
    
    def detect_wake_word(self, transcription: str) -> bool:
        """Detect if the wake word 'edith' is present in the transcription."""
        return "edith" in transcription.lower()

    def start_conversation(self) -> None:
        """Initialize conversation state."""
        logging.info("Wake word detected...")
        self.is_in_conversation = True
        self.last_interaction_time = datetime.datetime.now()

    def is_within_timeout(self) -> bool:
        """Check if the conversation is still within timeout."""
        return (datetime.datetime.now() - self.last_interaction_time).total_seconds() < self.conversation_timeout

    def launch(self):
        logging.info("Launching Edith...")
        try:
            while True:
                if self.play_obj and self.play_obj.is_playing():
                    pass  # Wait while audio is playing
                # Capture audio and get transcription
                audio_file = record_audio()
                transcription = transcribe_audio(audio_file)

                if transcription:
                    transcription = self.clean_text(transcription).lower()
                    print("Transcription:", transcription)  # Debugging output
                    # Process commands or questions
                    self.process_transcription(transcription)
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def process_transcription(self, transcription: str):
        """Check and handle the transcription for commands or questions."""
        if "access bios" in transcription:
            self.settings_menu()
            return

        if self.detect_wake_word(transcription):
            self.start_conversation()

        if self.is_in_conversation and self.is_within_timeout():
            self.handle_transcription(transcription)
        else:
            self.is_in_conversation = False

    def handle_transcription(self, transcription: str):
        """Process the transcription for commands or questions."""
        logging.info(f"Received transcription: {transcription}")

        if self.check_ghost_net_protocol(transcription):
            logging.info("Ghost Net Protocol command detected.")
            return

        if self.check_document_analysis(transcription):
            logging.info("Document analysis command detected.")
            return
        
        # Fallback response
        logging.info("Generating fallback response.")
        response = self.convert_decimal_to_verbal(self.handle_conversation(transcription))
        self.speak(response)


    def check_ghost_net_protocol(self, transcription: str) -> bool:
        """Check for Ghost Net Protocol commands."""
        ghost_net_bundles = [
            ['enable', 'ghost', 'net', 'protocol'],
            ['activate', 'ghost', 'net', 'protocol'],
            ['disable', 'ghost', 'net', 'protocol'],
            ['deactivate', 'ghost', 'net', 'protocol'],
            ['override', 'ghost', 'net', 'protocol'],
            ['start', 'ghost', 'net', 'protocol'],
            ['stop', 'ghost', 'net', 'protocol'],
        ]

        for bundle in ghost_net_bundles:
            if all(keyword in transcription for keyword in bundle):
                self.handle_ghost_net_protocol(bundle, transcription)
                return True
        return False

    def check_document_analysis(self, transcription: str) -> bool:
        """Check for Document Analysis commands."""
        document_analysis_bundles = [
            ['perform', 'document', 'analysis'],
            ['conduct', 'document', 'analysis'],
            ['analyze', 'document'],
        ]

        for bundle in document_analysis_bundles:
            if all(keyword in transcription for keyword in bundle):
                self.perform_document_analysis()
                return True
        return False
    
    def handle_ghost_net_protocol(self, bundle: list, transcription: str):
        """Handle Ghost Net Protocol commands."""
        if any(command in bundle for command in ['disable', 'deactivate', 'override']):
            password = self.get_text_after_keyword(transcription, 'password')
            keyword = self.get_text_after_keyword(transcription, 'keyword')
            if password or keyword:
                text_to_speech("Disabling ghost net protocol")
                override(True, password or keyword)
            else:
                print("No valid keyword found to extract text.")
        else:
            enable_protocol()  # Enable or activate the protocol

    def perform_document_analysis(self):
        """Handle document analysis requests."""
        logging.info("Document analysis triggered.")
        try:
            contents = extract_file_contents()
            response = self.convert_decimal_to_verbal(
                self.handle_conversation(f'Analyze this document and give me a brief explanation and further information regarding the document: "{contents}"')
            )
            self.speak(response)
        except Exception as e:
            logging.error(f"Error during document analysis: {e}")


if __name__ == "__main__":
# def main() -> None:
    edith = EdithMainframe()
# while True:
    edith.launch()

