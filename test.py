from transformers import pipeline

# Create the text generation pipeline using the "gpt2" model
pipe = pipeline("text-generation", model="gpt2")


def qna_chatbot(prompt):
    # Generate a response based on the input prompt
    generated_text = pipe(prompt, max_length=100, num_return_sequences=1)[0][
        "generated_text"
    ]

    # Extract the answer from the generated text
    answer = generated_text[len(prompt) :].strip()

    return answer


print("Q&A Chatbot:")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = qna_chatbot(user_input)
    print("Chatbot:", response)
