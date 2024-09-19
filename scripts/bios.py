import time
import random
import subprocess
import os
import shutil
import sqlite3
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ANSI color escape codes
RED = "\033[91m"
RESET = "\033[0m"

def print_red(text):
    """Prints text in red color for error messages."""
    print(f"{RED}{text}{RESET}")

def get_size(file_path):
    """Returns the size of the file in a human-readable format.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Size of the file in MB, or '0MB' if not found.
    """
    try:
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            return f"{size / (1024 * 1024):.2f}MB"  # Convert bytes to MB
    except Exception as e:
        logging.error(f"Unable to get size for '{file_path}': {e}")
    return "0MB"

modules = {
    "Text-to-speech Model": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/data/models/jenny_model/model.pt",
    },
    "Speech recognition": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/speech_to_text.py",
    },
    "Text-to-speech (TTS)": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/jenny_tts.py",
    },
    "Natural language processing": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/data/data.pth",
    },
    "Large Language Model": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/large_language_model/llm_main.py",
    },
    "Network tools": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/network_tools.py",
    },
    "Hardware diagnostics": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/system_info.py",
    },
    "Peripheral devices": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/system_info.py",
    },
    "Audio processing": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/cerebral_matrix.py",
    },
    "Security modules": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/modules/barn_door_protocol.py",
    },
    "Virtual Assistant": {
        "loaded": False,
        "progress": 0,
        "file_path": "scripts/edith/cerebral_matrix.py",
    },
}

# Add size to each module
for module in modules.values():
    module["size"] = get_size(module["file_path"])

def load_modules():
    """Loads each module and handles errors."""
    logging.info("IOS (Basic Input/Output System) initializing...")
    time.sleep(1.5)

    with tqdm(total=len(modules), desc="Loading modules", unit="module", ascii=True) as pbar:
        for module_name, module_info in modules.items():
            try:
                if not os.path.isfile(module_info["file_path"]):
                    print_red(f"ERROR: {module_name} file '{module_info['file_path']}' not found.")
                    continue

                time.sleep(random.uniform(0.2, 0.5))

                # Simulated error handling
                if random.random() < 0.2:
                    print_red(f"ERROR: {module_name} failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))
                    logging.info(f"Attempting to fix {module_name}...")
                    time.sleep(random.uniform(0.3, 0.6))
                    logging.info(f"{module_name} fixed.")

                module_info["loaded"] = True
                module_info["progress"] = 100
                pbar.update(1)
                logging.info(f"INIT: {module_name} loaded successfully. Size: {module_info['size']}")

            except Exception as e:
                print_red(f"ERROR: An error occurred while loading '{module_name}': {e}")
                continue  # Continue with the next module

    logging.info("INIT: All components initialized. Edith is now operational.")

def run_script():
    """Runs the main script after all components are initialized."""
    max_retries = 3
    for attempt in range(max_retries):
        logging.info("Initializing edith...")
        try:
            script_path = "scripts/edith/cerebral_matrix.py"
            subprocess.run(["python", script_path], check=True)
            logging.info("Script execution completed.")
            break  # Exit loop if successful
        except subprocess.CalledProcessError as e:
            print_red(f"Script execution failed with error: {e}")
            if attempt < max_retries - 1:
                logging.info("INFO: Retrying script execution...")
                time.sleep(2)  # Wait before retrying
            else:
                print_red("ERROR: Script execution failed after multiple attempts.")

def bios_boot():
    """Main function to simulate BIOS boot sequence."""
    logging.info("Starting Friday AI boot sequence...")
    time.sleep(1)
    try:
        load_modules()
        if all(module["loaded"] for module in modules.values()):
            run_script()
    except Exception as e:
        print_red(f"An unexpected error occurred during boot: {e}")

if __name__ == "__main__":
    bios_boot()
