import os

def create_file_or_folder(input_string, destination=None):
    # Extracting the file or folder name from the input string
    start_index_named = input_string.find("named") + len("named") + 1
    start_index_called = input_string.find("called") + len("called") + 1
    start_index = max(start_index_named, start_index_called)
    end_index = len(input_string)
    name = input_string[start_index:end_index].strip()

    if 'file' in input_string:
        if 'dot' in input_string:
            # Create a file with specified extension
            start_index_dot = input_string.find("dot") + len("dot") + 1
            extension = input_string[start_index_dot:].strip()
        elif 'python' in input_string:
            extension = 'py'
        elif 'text' in input_string:
            extension = 'txt'
        elif 'executable' in input_string or 'exe' in input_string:
            extension = 'exe'
        else:
            extension = 'txt'

        filename = name + '.' + extension

        if destination:
            filename = os.path.join(destination, filename)

        with open(filename, 'w'):
            pass
        print(f"File '{filename}' has been created.")
    elif 'folder' in input_string:
        if destination:
            folder_path = os.path.join(destination, name)
            os.makedirs(folder_path)
            return (f"Folder '{folder_path}' has been created.")
        else:
            os.makedirs(name)
            print(f"Folder '{name}' has been created.")
    else:
        return ("Please specify whether to create a file or a folder.")

# Usage example
def create(input_str):
    create_file_or_folder(input_str, destination='C://Users//Alan M. Turing')
