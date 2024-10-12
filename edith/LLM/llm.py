import datetime
import logging
import os
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

warnings.filterwarnings("ignore", category=RuntimeWarning, module='networkx')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize language model
model = OllamaLLM(model="llama3.1")

with open('edith/LLM/llm_template.txt', 'r') as file:
    contents = file.read()
    template = f"""{contents}"""

# Define the chat prompt template

# File System Structure: {fs} (for reference only)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
class EdithMainframe:
    def __init__(self):
        logging.info("Initializing Edith Mainframe.")
        load_modules()
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

        if self.check_ghost_net_protocol(transcription):
            logging.info("Ghost Net Protocol command detected.")
            return

        if self.check_document_analysis(transcription):
            logging.info("Document Analysis command detected.")
            return
            
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

    # Command Processing
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
