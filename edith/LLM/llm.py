import datetime
import logging
import os
import sys
import warnings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from modules.settings_manager import SettingsManager
from modules.chat_history import ChatHistory
from modules.system_info import SystemInfo
from modules.text_processing import TextProcessing
from modules.jenny_tts import text_to_speech
from modules.ghostnet_protocol import override, enable_protocol
from modules.data_extraction import extract_file_contents
from modules.speech_to_text import record_audio, transcribe_audio
from modules.load_modules import get_size, modules, load_modules
from modules.intent_nlp import classify_intent
from modules.dvp import dvp

warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

system_info = SystemInfo()

gpu = system_info.get_gpu_info()
mem = system_info.get_memory_info()
# Assuming `mem` is the dictionary for memory details
# Extract and convert memory values
total_memory = int(float(mem['Total Memory'].replace('GB', '').strip()))
gpu_memory = gpu[0]['Memory Total']  # Accessing the first GPU's memory
gpu_memory = int(float(gpu_memory.replace('MB', '').strip()))  # Convert to int

# Print the memory values for verification
print(f"Total Memory: {total_memory} GB")
print(f"GPU Memory: {gpu_memory} MB")

# Condition check
if (gpu_memory < 3000 and total_memory < 16) or gpu_memory < 3000 or total_memory < 16:
    print("Conditions not met: either GPU memory is low or total memory is low.")
    model = "tinyllama"
    template = ""
else:
    print("Conditions met - Using llama3.1 with system features")
    model = 'llama3.1'
    with open('edith/LLM/llm_template.txt', 'r') as file:
        contents = file.read()
        template = f"""{contents}"""
    


print(model)
# Initialize language model
model = OllamaLLM(model=model)

# File System Structure: {fs} (for reference only)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
class EdithMainframe:
    def __init__(self):
        logging.info("Initializing Edith Mainframe.")
        # load_modules()
        self.chat_history = ChatHistory("edith/data/dialogue/dialogue_history.json")
        self.text_processing = TextProcessing()
        self.system_info = SystemInfo()
        self.settings_manager = SettingsManager()
        self.settings_manager.load_settings()
        self.play_obj = None
        self.output_path = None
        self.is_in_conversation = False
        self.last_interaction_time = datetime.datetime.now()

    # Public Methods
    def launch(self):
        logging.info("Launching Edith...")
        try:
            while True:
                if self.play_obj and self.play_obj.is_playing():
                    # Wait while audio is playing
                    # continue  # Skip to the next iteration of the loop
                    continue
                # Capture audio and get transcription only if not playing
                audio_file = record_audio()
                transcription = transcribe_audio(audio_file)

                if transcription:
                    transcription = self.text_processing.clean_text(transcription).lower()
                    print("Transcription:", transcription)  # Debugging output
                    # Process commands or questions
                    self.process_transcription(transcription)
        except Exception as e:
            logging.error("An error occurred: %s", e)


    def process_transcription(self, transcription: str):
        """Check and handle the transcription for commands or questions."""
        if "access bios" in transcription:
            self.settings_manager.settings_menu()
            return

        if self.text_processing.detect_wake_word(transcription):
            self.start_conversation()

        if self.is_in_conversation and self.is_within_timeout():
            self.handle_transcription(transcription)
        else:
            self.is_in_conversation = False

    def handle_transcription(self, transcription: str):
        """Process the transcription for commands or questions."""
        logging.info(f"Received transcription: {transcription}")
        response, result = classify_intent(transcription)
        print(response)
        if result==True:
            if response=='document_analysis_run':
                logging.info("Document Analysis response detected.")
                self.perform_document_analysis()
            elif response=="ghostnet_protocol":
                logging.info("Ghost Net Protocol response detected.")
            elif response=="log_request":
                logging.info("Log request detected.")
                chat_history = self.chat_history.load_chat_history()
                
                if chat_history:
                    last_entry = chat_history[-1]  # Get the last chat entry
                    log_entry = f"{last_entry['timestamp']} | User: {last_entry['User']} | AI: {last_entry['AI']}"

                    home_dir = os.path.expanduser("~")
    
                    # Define the directory path
                    settings_dir = os.path.join(home_dir, 'edith_config')
                    
                    # Create the directory if it doesn't exist
                    os.makedirs(settings_dir, exist_ok=True)
                    
                    # Define the full path for the settings file
                    log_file_path = os.path.join(settings_dir, '/log_requests.json')
            elif response=="data_visualization_started":
                try:
                    # Perform data visualization
                    logging.info("Data visualization started.")
                    self.speak("Will do, sir")
                    dvp()
                except Exception as e:
                    logging.error("Failed to perform data visualization: {e}")
                    pass


        else:
            # Fallback response
            logging.info("Generating fallback response.")
            response = self.text_processing.convert_decimal_to_verbal(self.handle_conversation(transcription))
            self.speak(response)

    # Audio Management
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

    # Conversation Management
    def start_conversation(self) -> None:
        """Initialize conversation state."""
        logging.info("Wake word detected...")
        self.is_in_conversation = True
        self.last_interaction_time = datetime.datetime.now()

    def is_within_timeout(self) -> bool:
        """Check if the conversation is still within timeout."""
        return (datetime.datetime.now() - self.last_interaction_time).total_seconds() < self.settings_manager.conversation_timeout

    # Conversation Handling
    def handle_conversation(self, user_input: str) -> str:
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

    def handle_ghost_net_protocol(self, bundle: list, transcription: str):
        """Handle Ghost Net Protocol commands."""
        
        # Keywords for disabling the protocol
        disable_keywords = [
            "disable",
            "deactivate",
            "stop",
            "override",
            "turn off",
            "halt",
            "shut down",
            "cease",
            "terminate",
            "suspend"
        ]
        
        # Check if any disable command is in the transcription
        if any(command in transcription.lower() for command in disable_keywords):
            password = self.get_text_after_keyword(transcription, 'password')
            keyword = self.get_text_after_keyword(transcription, 'keyword')
            
            if password or keyword:
                text_to_speech("Disabling ghost net protocol")
                override(True, password or keyword)
            else:
                print("No valid keyword found to extract text for disabling the protocol.")
        
        else:
            # Enable or activate the protocol
            text_to_speech("Enabling ghost net protocol")
            enable_protocol()


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
            logging.error(f"Error during document analysis: {e}")



if __name__ == "__main__":
    edith = EdithMainframe()
    edith.launch()
