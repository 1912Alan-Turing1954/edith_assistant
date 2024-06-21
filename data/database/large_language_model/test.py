import torch
from transformers import pipeline, set_seed

# Set seed for reproducibility
set_seed(42)

# Example usage:
messages = [
    {
        "role": "system",
        "content": "",
    },
    {"role": "user", "content": ""},
]


def generate_responses(
    messages,
    model_name="Qwen/Qwen2-7B-Instruct",
    max_new_tokens=50,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    repetition_penalty=1.0,
):
    """
    Generates responses to a list of messages using a specified model.

    Args:
        messages (list): A list of dictionaries where each dictionary contains keys 'role' and 'content'.
        model_name (str): The name of the model to use for text generation. Default is "Qwen/Qwen2-7B-Instruct".
        max_new_tokens (int): The maximum number of tokens to generate for each response. Default is 50.
        device (int or str): The GPU device to run the model on. Use -1 for CPU, 0 or 'cuda:0' for GPU. Default is 0.

    Returns:
        list: A list of generated responses.
    """
    pipe = pipeline("text-generation", model=model_name)
    # pipe = pipeline(
    #     "text-generation",
    #     model="microsoft/Phi-3-mini-4k-instruct",
    #     trust_remote_code=True,
    #     device=device,
    # )
    responses = pipe(
        messages,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
    )
    return [response["generated_text"] for response in responses]


def edith_ai(input_text):
    with open("Data/boot_personality_prompt.txt", "r") as f:
        prompt = f.read()
        print(prompt)

    messages[1]["content"] = ""
    messages[0]["content"] += prompt
    messages[1]["content"] += input_text

    responses = generate_responses(messages)
    for response in responses:
        print(response)

    # Debugging statement
    print("User input:", input_text)

    return response[2]["content"]


if __name__ == "__main__":
    # Determine device availability
    # device = 0 if torch.cuda.is_available() else 1  # Use GPU if available, else CPU

    while True:
        user_input = input("input: ")
        edith_ai(user_input)
