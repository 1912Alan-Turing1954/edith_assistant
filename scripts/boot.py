import time
import random
import subprocess
import os
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ANSI color escape codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_red(text):
    """Prints text in red color for error messages."""
    print(f"{RED}{text}{RESET}")

def get_size(file_path):
    """Returns the size of the file in a human-readable format."""
    try:
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            return f"{size / (1024 * 1024):.2f}MB"  # Convert bytes to MB
    except Exception as e:
        logging.error(f"Unable to get size for '{file_path}': {e}")
    return "0MB"

modules = {
    "🔊 Text-to-Speech Model": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/data/models/jenny_model/model.pt",
    },
    "🗣 Speech Recognition": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/speech_to_text.py",
    },
    "🎤 Audio Processing": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/cerebral_matrix.py",
    },
    "🔍 Natural Language Processing": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/data/data.pth",
    },
    "🧠 Large Language Model": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/large_language_model/llm_main.py",
    },
    "🌐 Network Tools": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/network_tools.py",
    },
    "⚙️ Hardware Diagnostics": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/system_info.py",
    },
    "🔒 Security Modules": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/barn_door_protocol.py",
    },
    "🤖 Virtual Assistant": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/cerebral_matrix.py",
    },
}

# Add size to each module
for module in modules.values():
    module["size"] = get_size(module["file_path"])

def load_modules():
    """Loads each module with enhanced loading animations."""
    logging.info("Initializing Quantum Operating System... Please wait...")
    time.sleep(1.5)

    with tqdm(total=len(modules), desc="Loading modules", unit="module", ascii=True) as pbar:
        for module_name, module_info in modules.items():
            try:
                if not os.path.isfile(module_info["file_path"]):
                    print_red(f"ERROR: {module_name} file '{module_info['file_path']}' not found.")
                    continue

                time.sleep(random.uniform(0.5, 1.0))
                logging.info(f"LOADING: {module_name} ({module_info['size']})...")

                # Simulate the loading effect
                for _ in range(5):
                    time.sleep(0.1)
                    pbar.set_postfix({"Current Module": module_name, "Status": "Initializing..."})
                    pbar.refresh()
                    time.sleep(0.1)

                # Simulated error handling
                if random.random() < 0.2:
                    print_red(f"ERROR: {module_name} failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))
                    logging.info(f"Attempting to rectify {module_name}...")
                    time.sleep(random.uniform(0.3, 0.6))
                    logging.info(f"STATUS: {module_name} successfully rectified.")

                module_info["loaded"] = True
                module_info["progress"] = 100
                pbar.update(1)
                logging.info(f"INIT: {module_name} loaded successfully.")

            except Exception as e:
                print_red(f"ERROR: An error occurred while loading '{module_name}': {e}")
                continue  # Continue with the next module

    logging.info("INIT: All systems are operational. AI is ready for engagement.")

def run_script():
    """Runs the main script after all components are initialized."""
    max_retries = 3
    for attempt in range(max_retries):
        logging.info("Booting up the virtual assistant...")
        try:
            script_path = "scripts/edith/cerebral_matrix.py"
            subprocess.run(["python", script_path], check=True)
            logging.info("Script execution completed successfully.")
            break  # Exit loop if successful
        except subprocess.CalledProcessError as e:
            print_red(f"ERROR: Script execution failed with error: {e}")
            if attempt < max_retries - 1:
                logging.info("INFO: Retrying script execution in 2 seconds...")
                time.sleep(2)  # Wait before retrying
            else:
                print_red("ERROR: Script execution failed after multiple attempts. Initiating shutdown protocols...")

def boot():
    """Main function to simulate BIOS boot sequence."""
    logging.info("Initiating AI boot sequence... Please stand by...")
    time.sleep(1)
    try:
        load_modules()
        if all(module["loaded"] for module in modules.values()):
            run_script()
    except Exception as e:
        print_red(f"ERROR: An unexpected error occurred during boot: {e}")

if __name__ == "__main__":
    boot()
