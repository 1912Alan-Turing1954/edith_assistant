# import tkinter as tk
# import threading
# import subprocess

# def run_script():
#     # Run your script and capture the output
#     result = subprocess.run(['python', 'edith/LLM/llm.py'], capture_output=True, text=True)
#     output_text.delete(1.0, tk.END)  # Clear previous output
#     output_text.insert(tk.END, result.stdout)  # Insert new output

# def start_script_thread():
#     thread = threading.Thread(target=run_script)
#     thread.start()  # Start the thread

# # Create the main window
# root = tk.Tk()
# root.title("LLM Script Output")

# # Button to run the script
# run_button = tk.Button(root, text="Run LLM Script", command=start_script_thread)
# run_button.pack(pady=10)

# # Text area to display output
# output_text = tk.Text(root, height=20, width=50)
# output_text.pack(pady=10)

# root.mainloop()
