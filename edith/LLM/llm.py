import datetime
import logging
import os
import sys
import warnings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from modules.settings_manager import SettingsManager, settings_gui
from modules.chat_history import ChatHistory
from modules.system_info import SystemInfo
from modules.text_processing import TextProcessing
from modules.jenny_tts import text_to_speech
from modules.data_extraction import extract_file_contents
from modules.speech_to_text import record_audio, transcribe_audio
from modules.load_modules import get_size, modules, load_modules
from modules.intent_nlp import classify_intent
from modules.map.map import map_main
from modules.dvp import dvp
from modules.task_manegment import task_manager

warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

system_info = SystemInfo()

# Get GPU and memory information
try:
    gpu = system_info.get_gpu_info()
    mem = system_info.get_memory_info()

    total_memory = int(float(mem['Total Memory'].replace('GB', '').strip()))
    gpu_memory = int(float(gpu[0]['Memory Total'].replace('MB', '').strip()))

    logging.info(f"Total Memory: {total_memory} GB")
    logging.info(f"GPU Memory: {gpu_memory} MB")

    if (gpu_memory < 3000 and total_memory < 16) or gpu_memory < 3000 or total_memory < 16:
        logging.warning("Conditions not met: either GPU memory or total memory is low.")
        model = "tinyllama"
        template = ""
    else:
        logging.info("Conditions met - Using llama3.1 with system features")
        model = 'llama3.1'
        with open('edith/LLM/llm_template.txt', 'r') as file:
            contents = file.read()
            template = f"""{contents}"""
except Exception as e:
    logging.error("Failed to retrieve system information: %s", e)
    sys.exit(1)

# Initialize language model
model = OllamaLLM(model=model)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class EdithMainframe:
    def __init__(self):
        logging.info("Initializing Edith Mainframe.")
        self.chat_history = ChatHistory("edith/data/dialogue/dialogue_history.json")
        self.text_processing = TextProcessing()
        self.system_info = SystemInfo()
        self.settings_manager = SettingsManager()
        self.settings_manager.load_settings()
        self.play_obj = None
        self.output_path = None
        self.is_in_conversation = False
        self.last_interaction_time = datetime.datetime.now()

    def launch(self):
        logging.info("Launching Edith...")
        try:
            while True:
                if self.play_obj and self.play_obj.is_playing():
                    continue
                
                audio_file = record_audio()
                transcription = transcribe_audio(audio_file)
                
                if transcription and self.is_text_input_command(transcription):
                    print("Switched to text input mode.")
                    transcription = input('You: ')
                
                if transcription:
                    transcription = self.text_processing.clean_text(transcription).lower()
                    logging.info("Transcription: %s", transcription)
                    self.process_transcription(transcription)
        except Exception as e:
            logging.error("An error occurred in launch: %s", e)

    def is_text_input_command(self, transcription: str) -> bool:
        """Check if the transcription is a command to switch to text input."""
        return any(command in transcription.lower() for command in ["text input", "text mode"])

    def process_transcription(self, transcription: str):
        """Check and handle the transcription for commands or questions."""
        try:
            if "access bios" in transcription:
                settings_gui()
                return

            if self.text_processing.detect_wake_word(transcription):
                self.start_conversation()

            if self.is_in_conversation and self.is_within_timeout():
                self.handle_transcription(transcription)
            else:
                self.is_in_conversation = False
        except Exception as e:
            logging.error("Error processing transcription: %s", e)

    def handle_transcription(self, transcription: str):
        """Process the transcription for commands or questions."""
        try:
            logging.info("Received transcription: %s", transcription)
            response, res, result = classify_intent(transcription)
            print(result)
            if result:
                self.handle_intent_response(response, res)
            else:
                logging.info("Generating fallback response.")
                response = self.text_processing.convert_decimal_to_verbal(self.handle_conversation(transcription))
                self.speak(response)
        except Exception as e:
            logging.error("Error handling transcription: %s", e)

    def handle_intent_response(self, response: str, res: str):
        """Handle different responses based on classified intent."""
        if response == 'document_analysis_run':
            logging.info("Document Analysis response detected.")
            self.speak(res)
            self.perform_document_analysis()
        elif response == "log_request":
            self.speak(res)
            self.handle_log_request()
        elif response == "data_visualization_started":
            self.speak(res)
            self.start_data_visualization()
        elif response=="task_manager_started":
            self.speak(res)
            task_manager()
        elif response == "open_map":
            self.speak(res)
            map_main()
        else:
            logging.warning(f"Unexpected response detected: {response}")
            self.speak("I'm not sure how to respond to that.")

    def handle_log_request(self):
        """Handle logging of the last chat entry."""
        try:
            logging.info("Log request detected.")
            chat_history = self.chat_history.load_chat_history()
            if chat_history:
                last_entry = chat_history[-1]  # Get the last chat entry
                log_entry = f"{last_entry['timestamp']} | User: {last_entry['User']} | AI: {last_entry['AI']}"
                self.save_log_entry(log_entry)
        except Exception as e:
            logging.error("Error handling log request: %s", e)

    def save_log_entry(self, log_entry: str):
        """Save log entry to a file."""
        home_dir = os.path.expanduser("~")
        settings_dir = os.path.join(home_dir, '.edith_config')
        os.makedirs(settings_dir, exist_ok=True)
        log_file_path = os.path.join(settings_dir, 'log_requests.json')

        try:
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_entry + "\n")
            logging.info("Log entry saved successfully.")
        except Exception as e:
            logging.error("Failed to save log entry: %s", e)

    def start_data_visualization(self):
        """Start data visualization process."""
        try:
            logging.info("Data visualization started.")
            dvp()
        except Exception as e:
            logging.error("Failed to perform data visualization: %s", e)

    def speak(self, input_: str) -> None:
        """Convert text to speech and manage audio playback."""
        self.stop_audio()
        self.play_obj, self.output_path = text_to_speech(input_)
        if self.output_path and os.path.exists(self.output_path):
            os.remove(self.output_path)

    def stop_audio(self) -> None:
        """Stop current audio playback and remove the output file if exists."""
        if self.play_obj and self.play_obj.is_playing():
            try:
                self.play_obj.stop()
                if self.output_path and os.path.exists(self.output_path):
                    os.remove(self.output_path)
                    logging.info("Stopped audio playback and removed output file.")
            except Exception as e:
                logging.error("Failed to stop audio or remove output file: %s", e)

    def start_conversation(self) -> None:
        """Initialize conversation state."""
        logging.info("Wake word detected...")
        self.is_in_conversation = True
        self.last_interaction_time = datetime.datetime.now()

    def is_within_timeout(self) -> bool:
        """Check if the conversation is still within timeout."""
        return (datetime.datetime.now() - self.last_interaction_time).total_seconds() < self.settings_manager.conversation_timeout

    def handle_conversation(self, user_input: str) -> str:
        """Handle the user's input in a conversation."""
        try:
            logging.info(f"Handling conversation input: {user_input}")
            self.stop_audio()
            print("Forwarding request to LLM...")

            if not user_input or not isinstance(user_input, str):
                logging.warning("Invalid user input received.")
                return "I'm sorry, I didn't understand that."

            chat_history = self.chat_history.load_chat_history()
            context_entries = chat_history[-2:] if len(chat_history) >= 2 else []
            context = "\n".join([f"{entry['User']}: {entry['AI']}" for entry in context_entries])
            logging.debug(f"Context for LLM: {context}")

            result = chain.invoke({
                "context": context,
                "system": self.system_info.get_system_info(),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "question": user_input
            })

            self.chat_history.update_chat_history(user_input, result)
            return result
        except Exception as e:
            logging.error("Error in handle_conversation: %s", e)
            return "I'm sorry, there was an error processing your request."

    def perform_document_analysis(self):
        """Handle document analysis requests."""
        logging.info("Document analysis triggered.")
        try:
            contents = extract_file_contents()  # or use a specific document based on user input
            response = self.text_processing.convert_decimal_to_verbal(
                self.handle_conversation(f'Analyze this document and give me a brief explanation: "{contents}"')
            )
            self.speak(response)
        except Exception as e:
            logging.error("Error during document analysis: %s", e)

if __name__ == "__main__":
    edith = EdithMainframe()
    edith.launch()

