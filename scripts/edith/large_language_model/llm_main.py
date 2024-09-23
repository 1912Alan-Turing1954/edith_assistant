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
from modules.jenny_tts import text_to_speech
from modules.ghostnet_protocol import override, enable_protocol
import speedtest

warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model = OllamaLLM(model="llama3.1")

template = """
Background Your name is Edith, you are an AI assistant, created by Logan. You are concise and direct, yet have a conversational tone. Keep responses brief—1-2 sentences—without unnecessary details or slang. You are supportive and intelligent, and professional, often displaying a caring demeanor. Additionally, you are loyal and resourceful, always ready to assist and provide guidance, reflecting a strong sense of reliability and companionship. Do not treat each encounter as if it is our first, only do so if the time stamp between my last response is quite large. Answer the question below.

User-name: Logan (or can be addressed as sir, whichever you choose).

Here is the conversation history: {context}

System Information: {system} (Memory reference only)(Do not mention in conversation)

Date/Time: {timestamp} (for reference only)(12 hour clock format)

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class EdithMainframe:
    def __init__(self):
        logging.info("Initializing Edith Mainframe.")
        self.w = None
        self.play_obj = None
        self.output_path = None
        self.is_in_conversation = False
        self.conversation_timeout = 90
        self.last_interaction_time = datetime.datetime.now()
        self.load_settings()
        self.json_file = "scripts/data/dialogue/dialogue_history.json"
        self.protection_password = 'henry'

    def get_system_info(self) -> None:
        logging.info("Gathering system information.")
        system_info = {}

        # Operating System
        system_info["Operating System"] = f"{platform.system()} {platform.release()}"
        system_info["Computer Name"] = platform.node()

        # CPU Information
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        system_info["CPU Info"] = {
            "Physical Cores": cpu_count_physical,
            "Total Cores": cpu_count_logical,
            "CPU Usage": cpu_usage,
        }

        # Memory Information
        memory = psutil.virtual_memory()
        system_info["Total Memory"] = f"{memory.total / (1024 ** 3):.2f} GB"
        system_info["Available Memory"] = f"{memory.available / (1024 ** 3):.2f} GB"
        system_info["Used Memory"] = f"{memory.used / (1024 ** 3):.2f} GB"
        system_info["Memory Usage"] = f"{memory.percent}%"

        # Disk Information
        system_info["Disk Info"] = []
        for partition in psutil.disk_partitions(all=False):
            partition_usage = psutil.disk_usage(partition.mountpoint)
            system_info["Disk Info"].append({
                "Drive": partition.device,
                "Mount Point": partition.mountpoint,
                "File System": partition.fstype,
                "Total Space": f"{partition_usage.total / (1024 ** 3):.2f} GB",
                "Used Space": f"{partition_usage.used / (1024 ** 3):.2f} GB",
                "Free Space": f"{partition_usage.free / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{partition_usage.percent}%",
            })

        # Network Information
        system_info["Network Info"] = []
        for interface, addresses in psutil.net_if_addrs().items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    system_info["Network Info"].append({
                        "Interface": interface,
                        "IP Address": address.address,
                        "Netmask": address.netmask,
                    })
                    break

        # System Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        system_info["Uptime"] = f"{uptime_seconds // 3600} hours {uptime_seconds % 3600 // 60} minutes"

        # Python Version
        system_info["Python Version"] = platform.python_version()

        # Kernel Version (Linux)
        if platform.system() == "Linux":
            system_info["Kernel Version"] = platform.uname().release

        # Battery Status (for laptops)
        battery = psutil.sensors_battery()
        if battery:
            system_info["Battery Status"] = {
                "Percentage": f"{battery.percent}%",
                "Plugged In": battery.power_plugged,
                "Time Left": f"{battery.secsleft // 60} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging"
            }

        # GPU Information
        try:
            gpus = GPUtil.getGPUs()
            system_info["GPU Info"] = [{
                "GPU ID": gpu.id,
                "Name": gpu.name,
                "Load": f"{gpu.load * 100}%",
                "Memory Total": f"{gpu.memoryTotal} MB",
                "Memory Free": f"{gpu.memoryFree} MB",
                "Memory Used": f"{gpu.memoryUsed} MB",
            } for gpu in gpus]
        except Exception as e:
            logging.error(f"Unable to retrieve GPU info: {str(e)}")
            system_info["GPU Info"] = "Unable to retrieve GPU info."
            
        return system_info


    def handle_conversation(self, user_input) -> str:
        logging.info(f"Handling conversation input: {user_input}")
        self.stop_audio()

        # Ensure user input is valid
        if not user_input or not isinstance(user_input, str):
            logging.warning("Invalid user input received.")
            return "I'm sorry, I didn't understand that."

        try:
            with open(self.json_file, 'r') as file:
                chat_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Error reading dialogue history: {e}. Starting with empty chat history.")
            chat_history = []

        # Get the last two entries
        context_entries = chat_history[-2:] if len(chat_history) >= 2 else chat_history
        context = "\n".join([f"{entry['User']}: {entry['AI']}" for entry in context_entries])
        
        logging.debug(f"Context for LLM: {context}")

        result = chain.invoke({
            "context": context,
            "system": self.get_system_info(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"), 
            "question": user_input
        })
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        new_entry = {
            "timestamp": timestamp,
            "User": user_input,
            "AI": result
        }

        # Add the new entry to the chat history
        chat_history.append(new_entry)

        # Write the updated data back to the JSON file
        try:
            with open(self.json_file, 'w') as file:
                json.dump(chat_history, file, indent=4)
            logging.info("Dialogue history updated successfully.")
        except Exception as e:
            logging.error(f"Failed to write to dialogue history: {e}")

        return result

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

    def save_settings(self) -> None:
        """Saves the current settings to a JSON file."""
        settings = {
            'conversation_timeout': self.conversation_timeout,
            'logging_level': logging.getLevelName(logging.root.level),
            'protection': self.protection_password  # Only save if it is set
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            logging.info("Settings saved successfully to 'settings.json'.")
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

    def settings_menu(self) -> None:
        """Display a sci-fi inspired BIOS settings menu with effects."""
        while True:
            print("\n" + "=" * 70)
            print("           ██████████ BIOS Settings Interface ██████████")
            print("=" * 70)
            print(" [1] Change Conversation Timeout (Current: {}s)".format(self.conversation_timeout))
            print(" [2] Change Logging Level (Current: {})".format(logging.getLevelName(logging.root.level)))
            print(" [3] Set Protection Password (Current: {})".format("Set" if self.command_password else "Not Set"))
            print(" [4] Save current settings to file")
            print(" [5] Exit Settings")
            print("=" * 70)

            choice = input(" Select an option [1-5]: ")

            if choice == "1":
                new_timeout = input(" Enter new conversation timeout in seconds: ")
                if new_timeout.isdigit():
                    self.conversation_timeout = int(new_timeout)
                    logging.info(f"Updated conversation timeout to {self.conversation_timeout}s.")
                    print(" ➤ Updating conversation timeout...", end='')
                    time.sleep(1)
                    print(" Updated to {} seconds.".format(self.conversation_timeout))
                else:
                    logging.warning("Invalid input for conversation timeout.")
                    print(" ❌ Invalid input. Please enter a valid integer.")
            elif choice == "2":
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
                    print(" ➤ Updating logging level...", end='')
                    time.sleep(1)
                    print(" Updated to {}.".format(new_logging_level))
                else:
                    logging.warning("Invalid logging level input.")
                    print(" ❌ Invalid logging level.")
            elif choice == "3":
                new_password = input(" Enter new protection password: ")
                self.protection_password = new_password
                logging.info("Command password has been set.")
                print(" ➤ Command password has been set.")

            elif choice == "4":
                logging.info("Saving current settings.")
                print(" ➤ Saving current settings...", end='')
                self.save_settings()
                print(" Settings saved.")
            elif choice == "5":
                logging.info("Exiting settings menu.")
                print(" Exiting settings menu.")
                break
            else:
                logging.warning("Invalid choice in settings menu.")
                print(" ❌ Invalid choice. Please select a valid option.")

    def speak(self, input) -> None:
        self.stop_audio()
        self.play_obj, self.output_path = text_to_speech(input)

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
        return " ".join(cleaned_words)
    
    def _replace_decimal(self, match) -> str:
        """Helper method to replace decimal match with verbal representation."""
        number = match.group(0)
        integer_part, decimal_part = number.split('.')
        return f"{integer_part} point {decimal_part}"

    def convert_decimal_to_verbal(self, sentence: str) -> str:
        """Convert decimal numbers in a sentence to verbal form."""
        return re.sub(r'\b\d+\.\d+\b', self._replace_decimal, sentence)

    def get_text_after_keyword(self, input_string, keyword):
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

    def launch(self) -> None:
        logging.info("Launching main interaction loop.")
        while True:
            try:
                ghost_net_bundles = [
                    ['enable', 'ghost', 'net', 'protocol'],
                    ['activate', 'ghost', 'net', 'protocol'],
                    ['initiate', 'ghost', 'net', 'protocol'],
                    ['override', 'ghost', 'net', 'protocol'],
                    ['disable', 'ghost', 'net', 'protocol'],
                    ['deactivate', 'ghost', 'net', 'protocol'],
                    ['start', 'ghost', 'net', 'protocol'],
                    ['launch', 'ghost', 'net', 'protocol'],
                    ['turn', 'on', 'ghost', 'net', 'protocol'],
                    ['turn', 'off', 'ghost', 'net', 'protocol'],
                    ['set', 'ghost', 'net', 'protocol', 'to', 'enabled'],
                    ['set', 'ghost', 'net', 'protocol', 'to', 'disabled'],
                    ['engage', 'ghost', 'net', 'protocol'],
                    ['execute', 'ghost', 'net', 'protocol'],
                    ['authorize', 'ghost', 'net', 'protocol'],
                    ['confirm', 'ghost', 'net', 'protocol'],
                    ['stop', 'ghost', 'net', 'protocol'],
                    ['pause', 'ghost', 'net', 'protocol'],
                    ['suspend', 'ghost', 'net', 'protocol'],
                    ['resume', 'ghost', 'net', 'protocol']
                ]
            
                transcription = input("Type: ")
                if "access bios" in self.clean_text(transcription).lower():
                    self.settings_menu()
                    continue
                
                if self.detect_wake_word(transcription):
                        self.start_conversation()
                    
                if self.is_in_conversation and self.is_within_timeout():
                    # Check for Ghost Net Protocol bundles
                    for bundle in ghost_net_bundles:
                        if all(keyword in transcription for keyword in bundle):
                            if 'disable' in bundle or 'deactivate' in bundle or 'override' in bundle:
                                # Handle disable/deactivate logic
                                password = self.get_text_after_keyword(transcription, 'password')
                                keyword = self.get_text_after_keyword(transcription, 'keyword')
                                if password or keyword:
                                    text_to_speech("Disabling ghost net protocol")
                                    override(True, password or keyword)
                                else:
                                    print("No valid keyword found to extract text.")
                            else:
                                enable_protocol()  # Enable or activate the protocol
                            break  # Exit after handling
                    else:
                        response = self.convert_decimal_to_verbal(self.handle_conversation(transcription))
                        self.speak(response)
                else:
                    self.is_in_conversation = False
            except Exception as e:
                logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    edith = EdithMainframe()
    edith.launch()
