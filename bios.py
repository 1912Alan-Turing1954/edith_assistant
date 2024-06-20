import time
import random
import subprocess
import os.path
from tqdm import tqdm

# ANSI color escape codes
RED = "\033[91m"
RESET = "\033[0m"

# Simulated module loading statuses and additional data
modules = {
    "Neural network model": {
        "loaded": False,
        "progress": 0,
        "size": "50MB",
        "file_path": "./Meta-Llama-3-8B-Instruct/config.json",
    },
    "Text-to-speech Model": {
        "loaded": False,
        "progress": 0,
        "size": "50MB",
        "file_path": "./data/models/model.pt",
    },
    "Speech recognition": {
        "loaded": False,
        "progress": 0,
        "size": "30MB",
        "file_path": "./edith/speech_to_text.py",  # Example path, replace with actual
    },
    "Text-to-speech (TTS)": {
        "loaded": False,
        "progress": 0,
        "size": "20MB",
        "file_path": "./edith/jenny_tts.py",  # Example path, replace with actual
    },
    "Natural language processing": {
        "loaded": False,
        "progress": 0,
        "size": "40MB",
        "file_path": "./edith/brain/model.py",  # Example path, replace with actual
    },
    "Network tools": {
        "loaded": False,
        "progress": 0,
        "size": "15MB",
        "file_path": "./edith/modules/network_tools.py",
    },
    "Database connection": {
        "loaded": False,
        "progress": 0,
        "size": "5MB",
        "file_path": "./edith/modules/database_connection.py",
    },
    "Hardware diagnostics": {
        "loaded": False,
        "progress": 0,
        "size": "25MB",
        "file_path": "./edith/modules/system_info.py",
    },
    "Peripheral devices": {
        "loaded": False,
        "progress": 0,
        "size": "12MB",
        "file_path": "./edith/modules/system_info.py",
    },
    "Audio processing": {
        "loaded": False,
        "progress": 0,
        "size": "18MB",
        "file_path": "./edith/jenny_tts.py",  # Example path, replace with actual
    },
    "Security modules": {
        "loaded": False,
        "progress": 0,
        "size": "8MB",
        "file_path": "./edith/modules/system_info.py",
    },
    "Data analytics": {
        "loaded": False,
        "progress": 0,
        "size": "22MB",
        "file_path": "./edith/modules/data_analytics.py",  # Example path, replace with actual
    },
    "Virtual Assistant": {
        "loaded": False,
        "progress": 0,
        "size": "22MB",
        "file_path": "./edith/edith_testing.py",  # Example path, replace with actual
    },
}


# Function to print in red
def print_red(text):
    print(f"{RED}{text}{RESET}")


# Function to simulate loading each module with progress bars and error handling
def load_modules():
    print("IOS (Basic Input/Output System) initializing...\n")
    time.sleep(1.5)  # Reduce the initial sleep time to 1.5 seconds

    try:
        # Define progress bar
        with tqdm(
            total=len(modules), desc="Loading modules", unit="module", ascii=True
        ) as pbar:
            for module_name, module_info in modules.items():
                # Check if file exists before attempting to load
                if not os.path.isfile(module_info["file_path"]):
                    print_red(
                        f"ERROR: {module_name} file '{module_info['file_path']}' not found."
                    )
                    continue

                # Simulate module loading time (faster loading)
                time.sleep(random.uniform(0.2, 0.5))  # Adjusted for faster loading

                # Introduce errors for specific modules (simulated)
                if module_name == "Speech recognition" and random.random() < 0.2:
                    print_red("ERROR: Speech recognition module failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Attempting to fix Speech recognition...")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Speech recognition fixed.")
                elif module_name == "Network tools" and random.random() < 0.2:
                    print_red("ERROR: Network tools module failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Attempting to fix Network tools...")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Network tool fixed.")
                elif module_name == "Security modules" and random.random() < 0.2:
                    print_red("ERROR: Security modules module failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Attempting to fix Security modules...")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Security modules fixed.")
                elif module_name == "Data analytics" and random.random() < 0.2:
                    print_red("ERROR: Data analytics module failed to load.")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Attempting to fix Data analytics...")
                    time.sleep(random.uniform(0.3, 0.6))  # Simulate fix attempt
                    print("INFO: Data analytics fixed.")

                # Mark module as loaded
                module_info["loaded"] = True
                module_info["progress"] = 100
                pbar.update(1)
                print(
                    f"INIT: {module_name} loaded successfully. Size: {module_info['size']}"
                )

        # Final initialization message
        print("\nINIT: All components initialized. Edith is now operational.")

    except Exception as e:
        print_red(f"\nERROR: {e}")
        print("INFO: Continuing with initialization despite errors.")


# Function to simulate running a script after successful boot
def run_script():
    print("\nRunning edith...")
    try:
        script_path = "./edith/edith_testing.py"  # Replace with your actual script path
        subprocess.run(["python", script_path], check=True)
        print("Script execution completed.")
    except subprocess.CalledProcessError as e:
        print_red(f"Script execution failed with error: {e}")


# Main function to simulate BIOS boot sequence
def bios_boot():
    print("Starting Friday AI boot sequence...\n")
    time.sleep(1)  # Reduce the initial sleep time to 1 second
    try:
        load_modules()
        if all(module["loaded"] for module in modules.values()):
            run_script()
    except Exception as e:
        print_red(f"An unexpected error occurred during boot: {e}")


# Execute the boot sequence
if __name__ == "__main__":
    bios_boot()
