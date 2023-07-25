import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

def main():
    # Replace 'path_to_your_model_directory' with the path to your pre-trained model directory
    model_path = 'path_to_your_model_directory'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForMaskedLM.from_pretrained(model_path)

    # Example prompt or question
    prompt = "What is the capital of France?"

    # Tokenize the input text and convert it to model input format
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted token IDs
    predicted_token_ids = torch.argmax(outputs.logits, dim=-1)

    # Decode the predicted token IDs to get the generated text
    generated_text = tokenizer.decode(predicted_token_ids[0], skip_special_tokens=True)

    print("Generated Context or Information:")
    print(generated_text)

if __name__ == "__main__":
    main()
