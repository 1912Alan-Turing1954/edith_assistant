import subprocess
import sys
import os


def install_dependencies():
    try:
        # Create a directory to store downloaded packages
        download_dir = "downloaded_packages"
        os.makedirs(download_dir, exist_ok=True)

        print("Installing dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )

        # Download torch, torchvision, torchaudio from the specified index URL

        # torch_download_command = [
        #     sys.executable,
        #     "-m",
        #     "pip",
        #     "download",
        #     "torch",
        #     "torchvision",
        #     "torchaudio",
        #     "--index-url",
        #     "https://download.pytorch.org/whl/cu181",
        #     "--dest",
        #     download_dir,
        # ]
        # subprocess.check_call(torch_download_command)

        # # Install torch, torchvision, torchaudio locally from the downloaded packages
        # torch_local_install_command = [
        #     sys.executable,
        #     "-m",
        #     "pip",
        #     "install",
        #     "--no-index",
        #     "--find-links",
        #     download_dir,
        #     "torch",
        #     "torchvision",
        #     "torchaudio",
        # ]
        # subprocess.check_call(torch_local_install_command)

        # Download all packages from requirements.txt and store them locally
        requirements_download_command = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--requirement",
            "requirements.txt",
            "--dest",
            download_dir,
        ]
        subprocess.check_call(requirements_download_command)

        # Install all packages from requirements.txt locally from the downloaded packages
        requirements_local_install_command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            download_dir,
            "-r",
            "requirements.txt",
        ]
        subprocess.check_call(requirements_local_install_command)

        # Clean up downloaded packages (optional)
        # os.system(f"rm -r {download_dir}")  # for Unix-like systems
        # os.system(f"rmdir /s /q {download_dir}")  # for Windows

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing dependencies: {e}")
        sys.exit(1)


def run_script():
    try:
        print("Running your_script.py...")
        subprocess.check_call([sys.executable, "mainframe/scripts/bios.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running bios.py: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install_dependencies()
    run_script()
