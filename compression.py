import os
import argparse
import lz4.frame
import concurrent.futures

CHUNK_SIZE = 1024 * 1024  # 1 MB chunk size


def compress_file(file_path, compressed_file):
    try:
        with open(file_path, "rb") as original_file:
            while True:
                chunk = original_file.read(CHUNK_SIZE)
                if not chunk:
                    break
                compressed_chunk = lz4.frame.compress(chunk)
                compressed_file.write(compressed_chunk)
        return True
    except Exception as e:
        print(f"Error compressing {file_path}: {str(e)}")
        return False


def compress_folder(input_path, output_file):
    try:
        with open(output_file, "wb") as compressed_file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for foldername, _, filenames in os.walk(input_path):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        future = executor.submit(
                            compress_file, file_path, compressed_file
                        )
                        futures.append(future)
                for future in concurrent.futures.as_completed(futures):
                    if not future.result():
                        return False
        return True
    except Exception as e:
        print(f"Error compressing folder {input_path}: {str(e)}")
        return False


def compress_folder_or_file(input_path, output_file):
    if os.path.isfile(input_path):
        try:
            with open(output_file, "wb") as compressed_file:
                compress_file(input_path, compressed_file)
                return True
        except Exception as e:
            print(f"Error compressing file {input_path}: {str(e)}")
            return False
    elif os.path.isdir(input_path):
        return compress_folder(input_path, output_file)
    else:
        print(f"Error: {input_path} is not a valid file or directory.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress folder or file using lz4.")
    parser.add_argument("input_path", help="Path to the folder or file to compress.")
    parser.add_argument("output_file", help="Output compressed file name.")

    args = parser.parse_args()

    input_path = args.input_path
    output_file = args.output_file

    if not output_file.endswith(".lz4"):
        output_file += ".lz4"  # Ensure output file ends with .lz4

    if compress_folder_or_file(input_path, output_file):
        print("Compression completed successfully.")
    else:
        print("Compression failed. Please check the input and try again.")
