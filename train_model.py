import datasets
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import warnings
from transformers import AdamW

# Suppress AdamW deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    # dataset = datasets.load_dataset("wikipedia", "20220301.en", split="train")
    dataset = datasets.load_dataset("ms_marco", 'v1.1', split="train")

    # Step 3: Preprocess the data
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def tokenize_function(example):
        # Extract the "passages" field from the example
        passages = example["passages"]

        # Extract the "passage_text" field from each dictionary in the "passages" list
        passage_texts = [passage["passage_text"] for passage in passages]

        # Tokenize each passage and combine them into a single list
        tokenized_passages = tokenizer(passage_texts, padding="max_length", truncation=True, return_tensors="pt", is_split_into_words=True)

        return tokenized_passages

    # Step 4: Tokenize the filtered dataset to add the required columns
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Step 5: Create the model for masked language modeling (MLM)
    model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

    training_args = TrainingArguments(
        per_device_train_batch_size=32,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        output_dir="model",
        logging_dir="logs",
        logging_steps=100,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, 
        mlm_probability=0.15,
        pad_to_multiple_of=32,  # Add this parameter to pad to multiple of 32
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
