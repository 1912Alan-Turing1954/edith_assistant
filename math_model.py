from transformers import BertTokenizer, BertForMaskedLM
import torch

def main():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU available.")
        print(torch.cuda.get_device_name(0))  # Prints the name of the first GPU
    else:
        device = torch.device("cpu")
        print("GPU not available. Using CPU.")

    # Load the pre-trained "math_pretrained_bert" model and tokenizer
    model_name = "math_pretrained_bert"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForMaskedLM.from_pretrained(model_name)
    model.to(device)
    model.eval()

    while True:
        # Get user input for a math problem
        user_input = input("Enter a math problem: ")
        if user_input.lower() == "exit":
            break

        # Tokenize the input for masked language modeling
        inputs = tokenizer(user_input, return_tensors="pt")
        inputs.to(device)

        # Use the model to predict the masked tokens
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted token IDs (masked positions in the input)
        masked_index = (inputs["input_ids"] == tokenizer.mask_token_id).nonzero().item()

        # Get the predicted token IDs for the masked positions
        predictions = outputs.logits[0, masked_index]

        # Get the token with the highest probability (predicted answer)
        predicted_token_id = torch.argmax(predictions).item()

        # Convert the predicted token ID back to the actual token (word)
        predicted_token = tokenizer.decode(predicted_token_id)

        # Print the predicted answer
        print("Predicted Answer:", predicted_token)

if __name__ == "__main__":
    main()
