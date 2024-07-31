import datetime
import re
import sqlite3
import ollama

def fetch_conv_():
    # Create SQLite database if not exists
    conn = sqlite3.connect("mainframe/scripts/data/database/archives/dialogue/dialogue_archive.db")
    cursor = conn.cursor()
    # Query to fetch the latest four conversations ordered by timestamp in descending order
    cursor.execute('''
        SELECT user_input, bot_response, timestamp
        FROM dialogue
        ORDER BY timestamp DESC
        LIMIT 8
    ''')
    # Fetch all the results from the executed query
    conversations = cursor.fetchall()
    return conversations

def llm(user_input):
    history = "This is our chat history. do not bring up details in the chat history unless is seems appropiate or until I ask." + str(fetch_conv_())

    # Read prompt from file
    with open('mainframe/scripts/data/database/prompts/boot_personality_prompt.txt') as f:
        prompt = f.read().strip()  # Ensure to strip any extra whitespace

    try:
        # Call ollama.chat to generate response
        print(prompt)
        response = ollama.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': prompt + history},
                {'role': 'user', 'content': user_input}
            ]
        )

        # Extract the response content
        response_content = response['message']['content']
        return response_content

    except Exception as e:
        print(f"Error in llm function: {e}")
        return None
    


def llm_main(user_input):

    response = (llm(user_input))

    return response


