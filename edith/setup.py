from cx_Freeze import setup, Executable

setup(
    name="Edith: AI Assistant",
    version="2.0",
    description=" A Personal LLM AI Assistant is designed to enhance productivity and streamline daily tasks. Using advanced natural language processing, it can understand and respond to various requests efficiently.",
    executables=[Executable("boot.py")]
)