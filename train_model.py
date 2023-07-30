import datasets
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling

print(torch.cuda.is_available())

print(torch.cuda.device_count())

print(torch.cuda.current_device())

def main():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU available.")
        print(torch.cuda.get_device_name(0))  # Prints the name of the first GPU
    else:
        device = torch.device("cpu")
        print("GPU not available. Using CPU.")

    # Step 1: Load the 'wikipedia' dataset with required columns
    dataset = datasets.load_dataset("wikipedia", "20220301.en", split="train")

    # Step 2: Keep only the 'id', 'title', and 'text' columns in the dataset
    dataset.set_format(type='torch', columns=['id', 'title', 'text'])

    # Step 3: Preprocess the data
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def tokenize_function(example):
        return tokenizer(example["text"], padding="max_length", truncation=True)

    # Step 4: Tokenize the filtered dataset to add the required columns
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Step 5: Create the model for masked language modeling (MLM)
    model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

    training_args = TrainingArguments(
        per_device_train_batch_size=8,  # Reduce batch size further
        gradient_accumulation_steps=8,  # Increase gradient accumulation steps
        num_train_epochs=3,
        output_dir="model",
        logging_dir="logs",
        logging_steps=100,
        fp16=True,
    )

    # Step 6: Initialize the data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, 
        mlm_probability=0.15,
        # No need to pass max_length here, as it was already handled during tokenization
        return_tensors="pt"  # Return PyTorch tensors
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,  # Use the tokenized dataset directly
        data_collator=data_collator,
    )

    # Step 6: Train the model on the masked text
    trainer.train()

    # Step 7: Save the trained model
    model.save_pretrained("model_jarvis")

if __name__ == "__main__":
    main()
