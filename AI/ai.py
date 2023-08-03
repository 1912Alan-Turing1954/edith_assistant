from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
from langchain.embeddings import HuggingFaceEmbeddings
import tiktoken

def initialize_chatbot():
    # Load GPT-3-based chatbot model and tokenizer
    chatbot_model_name = 'h2oai/h2ogpt-oasst1-512-12b'
    chatbot_model = AutoModelForCausalLM.from_pretrained(chatbot_model_name)
    chatbot_tokenizer = AutoTokenizer.from_pretrained(chatbot_model_name)

    # Load reward model and tokenizer
    reward_model_name = 'OpenAssistant/reward-model-deberta-v3-large-v2'
    reward_model = AutoModelForSequenceClassification.from_pretrained(reward_model_name)
    reward_tokenizer = AutoTokenizer.from_pretrained(reward_model_name)

    # Load sentence embedding model
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs='cpu')

    # Configure tokenization settings (if needed)
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    return chatbot_model, chatbot_tokenizer, reward_model, reward_tokenizer, embedding_model

def generate_response(chatbot_model, chatbot_tokenizer, user_input):
    # Generate chatbot response using the chatbot model and tokenizer
    inputs = chatbot_tokenizer(user_input, return_tensors="pt")
    outputs = chatbot_model.generate(**inputs)
    response = chatbot_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

def calculate_reward(reward_model, reward_tokenizer, response):
    # Calculate reward for the generated response using the reward model and tokenizer
    inputs = reward_tokenizer(response, return_tensors="pt")
    outputs = reward_model(**inputs)
    reward = outputs.logits.softmax(dim=1)[0][1].item()  # Assuming class 1 is the positive reward class

    return reward

if __name__ == "__main__":
    chatbot_model, chatbot_tokenizer, reward_model, reward_tokenizer, embedding_model = initialize_chatbot()

    print("Chatbot: Hi! I am your chatbot assistant. How can I help you? (Type 'exit' to end the conversation)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Have a great day!")
            break

        # Generate chatbot response
        chatbot_response = generate_response(chatbot_model, chatbot_tokenizer, user_input)

        # Calculate reward for the chatbot response
        reward = calculate_reward(reward_model, reward_tokenizer, chatbot_response)

        print("Chatbot:", chatbot_response)
        print("Reward:", reward)