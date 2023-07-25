import datasets
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling

def main():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU available.")
        print(torch.cuda.get_device_name(0))  # Prints the name of the first GPU
    else:
        device = torch.device("cpu")
        print("GPU not available. Using CPU.")

    # Step 1: Load the 'triviaqa' dataset with required columns
    dataset = datasets.load_dataset("trivia_qa", "rc", split="train")

    # Step 2: Keep only the 'question', 'question_id', and 'answer' columns in the dataset
    dataset.set_format(type='torch', columns=['question_id', 'question', 'answer'])

    # Step 3: Preprocess the data
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")

    def tokenize_function(example):
        question = example["question"]
        inputs = tokenizer.encode_plus(question, padding="max_length", truncation=True, add_special_tokens=True)
        input_ids = inputs["input_ids"]

        # Mask 15% of the tokens for MLM training
        masked_indices = torch.bernoulli(torch.full(input_ids.shape, 0.15)).bool()
        masked_indices[0] = False  # Do not mask the [CLS] token
        input_ids[masked_indices] = tokenizer.mask_token_id

        labels = input_ids.clone()
        labels[~masked_indices] = -100  # Set the labels for non-masked tokens to -100

        return {
            "input_ids": input_ids,
            "attention_mask": inputs["attention_mask"],
            "labels": labels,
        }

    # Step 4: Tokenize the filtered dataset to add the required columns
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Save the tokenizer vocabulary
    tokenizer.save_pretrained("model_qa")

    # Step 5: Create the model for masked language modeling (MLM)
    model = AutoModelForMaskedLM.from_pretrained("roberta-base")

    training_args = TrainingArguments(
        per_device_train_batch_size=32,
        num_train_epochs=3,
        output_dir="model",
        logging_dir="logs",
        logging_steps=100,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, 
        mlm_probability=0.15,
        padding=True,
        max_length=128,  # Set your desired maximum length for the model input
        return_tensors="pt"  # Return PyTorch tensors
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,  # Use the tokenized dataset directly
        data_collator=data_collator,
        device=device,  # Specify the device to use (GPU or CPU)
    )

    # Step 6: Train the model on the masked text
    trainer.train()

    # Step 7: Save the trained model
    model.save_pretrained("model_qa")

if __name__ == "__main__":
    main()
