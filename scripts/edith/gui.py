import tkinter as tk
from tkinter import scrolledtext
import subprocess

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edith")
        self.root.geometry("400x300")

        # Create a scrolled text area for output
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

        # Run the script and display output
        self.run_script()

    def run_script(self):
        try:
            # Replace with the path to your script
            result = subprocess.run(['python', 'edith/cerebral_matrix.py'], capture_output=True, text=True)
            self.text_area.insert(tk.END, result.stdout + result.stderr)
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running script: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
