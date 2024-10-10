import os
import shutil
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(file_path):
    """Read content from a specified file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Read file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def write_file(file_path, content):
    """Write content to a specified file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f"Wrote to file: {file_path}")
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")

def move_file(source, destination):
    """Move a file from source to destination."""
    try:
        shutil.move(source, destination)
        logging.info(f"Moved file from {source} to {destination}")
    except Exception as e:
        logging.error(f"Error moving file from {source} to {destination}: {e}")

def delete_file(file_path):
    """Delete a specified file."""
    try:
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {e}")

# def list_files(folder_path):
#     """List all files in a specified folder."""
#     try:
#         files = os.listdir(folder_path)
#         logging.info(f"Listed files in: {folder_path}")
#         return files
#     except Exception as e:
#         logging.error(f"Error listing files in {folder_path}: {e}")
#         return []

# def find_files(partial_filename, search_path):
#     """Find all files matching a partial name in a specified directory."""
#     matching_files = []
#     for root, dirs, files in os.walk(search_path):
#         for file in files:
#             if partial_filename in file:
#                 matching_files.append(os.path.join(root, file))
#     return matching_files

def explore_directory(directory):
    """Explore the directory and return a mapping of folders."""
    directory_map = {}
    for root, dirs, files in os.walk(directory):
        directory_map[root] = files
    return directory_map

def resolve_directory(command, directory_map):
    """Resolve common directory names to actual paths."""
    home_dir = os.path.expanduser("~")
    if "home" in command:
        return home_dir
    elif "documents" in command:
        return os.path.join(home_dir, "Documents")
    elif "downloads" in command:
        return os.path.join(home_dir, "Downloads")
    elif "desktop" in command:
        return os.path.join(home_dir, "Desktop")
    else:
        for dir_name in directory_map.keys():
            if dir_name in command:
                return dir_name
        return home_dir  # Default to home directory if unrecognized

def process_fs_command(command):
    """Process user command and execute appropriate file operation."""
    command = command.lower().strip()

    if command.startswith("read"):
        file_path = command.split("read ")[1]
        return read_file(file_path)

    elif command.startswith("write"):
        parts = command.split("write ")[1].split(" to ")
        content = parts[0]
        file_path = parts[1]
        write_file(file_path, content)
        return f"Wrote to {file_path}"

    elif command.startswith("move"):
        parts = command.split("move ")[1].split(" to ")
        source = parts[0]
        destination = parts[1]
        move_file(source, destination)
        return f"Moved {source} to {destination}"

    elif command.startswith("delete"):
        file_path = command.split("delete ")[1]
        delete_file(file_path)
        return f"Deleted {file_path}"

    # elif "list" in command:
    #     directory = resolve_directory(command, directory_map)
    #     files = list_files(directory)
    #     return f"Files in {directory}: {', '.join(files)}" if files else f"No files found in {directory}."

    # elif "where is" in command:
    #     filename = command.split("where is ")[1]
    #     search_path = os.getcwd()  # Default search path is current working directory
    #     found_files = find_files(filename, search_path)

    #     return f"Files found matching '{filename}': {', '.join(found_files)}" if found_files else f"{filename} not found."

    else:
        return "Unknown command"
