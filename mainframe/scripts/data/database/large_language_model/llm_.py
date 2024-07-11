import re
import ollama

def llm(user_input):
    # Read prompt from file
    with open('mainframe/scripts/data/database/prompts/boot_personality_prompt.txt') as f:
        prompt = f.read().strip()  # Ensure to strip any extra whitespace

    try:
        # Call ollama.chat to generate response
        response = ollama.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': prompt},
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

while True:
    text = input("")
    print(llm_main(text))