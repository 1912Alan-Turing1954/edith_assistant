import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForSequenceClassification
from langchain.embeddings import HuggingFaceEmbeddings
import tiktoken

def initialize_chatbot():
    # Check if GPU is available, otherwise use CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load GPT-2.5-based chatbot model and tokenizer on GPU/CPU
    chatbot_model_name = 'EleutherAI/gpt-neo-1.3B'
    chatbot_tokenizer = GPT2Tokenizer.from_pretrained(chatbot_model_name)
    chatbot_model = GPT2LMHeadModel.from_pretrained(chatbot_model_name).to(device)

    # Load reward model and tokenizer on GPU/CPU
    reward_model_name = 'OpenAssistant/reward-model-deberta-v3-large-v2'
    reward_tokenizer = AutoTokenizer.from_pretrained(reward_model_name, max_length=512)
    reward_model = AutoModelForSequenceClassification.from_pretrained(reward_model_name).to(device)

    # Load sentence embedding model on GPU/CPU
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs=device)

    # Configure tokenization settings (if needed)
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-2.5-turbo")

    return chatbot_model, chatbot_tokenizer, reward_model, reward_tokenizer, embedding_model, device

def generate_response(chatbot_model, chatbot_tokenizer, user_input, device):
    # Generate chatbot response using the chatbot model and tokenizer
    inputs = chatbot_tokenizer(user_input, return_tensors="pt", max_length=512).to(device)
    outputs = chatbot_model.generate(**inputs)
    response = chatbot_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

def calculate_reward(reward_model, reward_tokenizer, response, device):
    # Calculate reward for the generated response using the reward model and tokenizer
    inputs = reward_tokenizer(response, return_tensors="pt", max_length=512).to(device)
    outputs = reward_model(**inputs)
    reward = outputs.logits.softmax(dim=1)[0][1].item()  # Assuming class 1 is the positive reward class

    return reward

if __name__ == "__main__":
    chatbot_model, chatbot_tokenizer, reward_model, reward_tokenizer, embedding_model, device = initialize_chatbot()

    print("Chatbot: Hi! I am your chatbot assistant. How can I help you? (Type 'exit' to end the conversation)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Have a great day!")
            break

        # Move user input and chatbot response to the GPU/CPU
        user_input = user_input.to(device)
        chatbot_response = generate_response(chatbot_model, chatbot_tokenizer, user_input, device)

        # Calculate reward for the chatbot response
        reward = calculate_reward(reward_model, reward_tokenizer, chatbot_response, device)

        print("Chatbot:", chatbot_response)
        print("Reward:", reward)
