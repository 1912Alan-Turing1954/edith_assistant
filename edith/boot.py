import shutil
import importlib.util
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
        "file_path": "edith/data/models/jenny_model/.model.pt",
    },
    "🗣 Speech Recognition": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/modules/speech_to_text.py",
    },
    "🎤 Audio Processing": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/modules/speech_to_text.py",
    },
    "🧠 Large Language Model": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/large_language_model/llm_main.py",
    },
    "⚙️ Hardware Diagnostics": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/large_language_model/llm_main.py",
    },
    "🔒 Security Modules": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/modules/ghostnet_protocol.py",
    },
    "🤖 Virtual Assistant": {
        "loaded": False,
        "progress": 0,
        "file_path": "edith/large_language_model/llm_main.py",
    },
}

# Add size to each module
for module in modules.values():
    module["size"] = get_size(module["file_path"])


def check_disk_space(min_required_space_mb):
    """Check if there is enough disk space available."""
    total, used, free = shutil.disk_usage("/")
    free_mb = free // (1024 * 1024)  # Convert bytes to MB
    if free_mb < min_required_space_mb:
        return False, free_mb
    return True, free_mb

def load_modules():
    """Loads each module with enhanced loading animations."""
    logging.info("Initializing Quantum Operating System... Please wait...")
    time.sleep(1.5)

    min_required_space_mb = 100  # Set a minimum required disk space in MB

    # Check for disk space
    space_available, free_space = check_disk_space(min_required_space_mb)
    if not space_available:
        print_red(f"ERROR: Not enough disk space available. Free space: {free_space} MB")
        return

    for module_name, module_info in modules.items():
        try:
            file_path = module_info["file_path"]

            # Create a progress bar for this module
            print(f" ➤ Loading {module_name}...", end='')
            with tqdm(total=100, desc=f"Loading {module_name}", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                for _ in range(100):
                        time.sleep(0.01)  # Simulate a delay
                        pbar.update(1)

            # Check if the file exists
            if not os.path.isfile(file_path):
                print_red(f"ERROR: {module_name} file '{file_path}' not found.")
                continue

            # Increment progress after existence check
            time.sleep(0.05)  # Quick sleep for feedback
            logging.info(f"Checked existence for {module_name}.")

            # Check if the file has read permissions
            if not os.access(file_path, os.R_OK):
                print_red(f"ERROR: {module_name} file '{file_path}' is not readable.")
                continue

            time.sleep(0.1)  # Slightly longer sleep for permission check
            logging.info(f"Checked permissions for {module_name}.")

            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                print_red(f"ERROR: {module_name} file '{file_path}' is empty.")
                continue

            time.sleep(0.15)  # Longer sleep for size check
            logging.info(f"Checked size for {module_name}.")

            # Log loading message
            logging.info(f"LOADING: {module_name} ({module_info['size']})...")
            time.sleep(random.uniform(0.15, 0.20))  # Simulate loading work

            # Mark module as loaded
            module_info["loaded"] = True
            module_info["progress"] = 100
            logging.info(f"INIT: {module_name} loaded successfully.")

        except Exception as e:
            print_red(f"ERROR: An error occurred while loading '{module_name}': {e}")
            continue  # Continue with the next module

    logging.info("INIT: All systems are operational. AI is ready for engagement.")



def run_script():
    """Runs the main script after all components are initialized."""
    max_retries = 3
    for attempt in range(max_retries):
        logging.info("Booting up virtual assistant...")
        try:
            script_path = "edith/large_language_model/llm_main.py"
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

