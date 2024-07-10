import re
import ollama

def llm(user_input):
    # Read prompt from file
    with open('mainframe/scripts/data/database/prompts/boot_personality_prompt.txt') as f:
        prompt = f.read().strip()  # Ensure to strip any extra whitespace

    try:
        # Call ollama.chat to generate response
        response = ollama.chat(
            model='llama2',
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
    
def remove_emoticons(response):
    # Define regex pattern to match expressions like *smiling* or (smiling)
    pattern = r'\*[\w\s]+\*|\([\w\s]+\)'
    
    # Use re.sub to replace matching patterns with an empty string
    clean_response = re.sub(pattern, '', response)
    
    return clean_response.strip()

def llm_main(user_input):

    response = remove_emoticons(llm(user_input))

    return response