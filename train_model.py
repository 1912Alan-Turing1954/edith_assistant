import datasets
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling

print(torch.cuda.is_available())

print(torch.cuda.device_count())

print(torch.cuda.current_device())

# def main():
#     if torch.cuda.is_available():
#         device = torch.device("cuda")
#         print("GPU available.")
#         print(torch.cuda.get_device_name(0))  # Prints the name of the first GPU
#     else:
#         device = torch.device("cpu")
#         print("GPU not available. Using CPU.")

#     # Step 1: Load the 'wikipedia' dataset with required columns
#     dataset = datasets.load_dataset("wikipedia", "20220301.en", split="train")

#     # Step 2: Keep only the 'id', 'title', and 'text' columns in the dataset
#     dataset.set_format(type='torch', columns=['id', 'title', 'text'])

#     # Step 3: Preprocess the data
#     tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

#     def tokenize_function(example):
#         return tokenizer(example["text"], padding="max_length", truncation=True)

#     # Step 4: Tokenize the filtered dataset to add the required columns
#     tokenized_dataset = dataset.map(tokenize_function, batched=True)

#     # Step 5: Create the model for masked language modeling (MLM)
#     model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

#     training_args = TrainingArguments(
#         per_device_train_batch_size=32,
#         gradient_accumulation_steps=4,  # Use gradient accumulation to simulate larger batch size
#         num_train_epochs=3,
#         output_dir="model",
#         logging_dir="logs",
#         logging_steps=100,
#         fp16=True,  # Use mixed precision training
#     )

#     data_collator = DataCollatorForLanguageModeling(
#         tokenizer=tokenizer, 
#         mlm_probability=0.15,
#         padding=True,
#         max_length=64,  # Reduce maximum sequence length to speed up training
#         return_tensors="pt"  # Return PyTorch tensors
#     )

#     trainer = Trainer(
#         model=model,
#         args=training_args,
#         train_dataset=tokenized_dataset,  # Use the tokenized dataset directly
#         data_collator=data_collator,
#         device=device,  # Specify the device to use (GPU or CPU)
#     )

#     # Step 6: Train the model on the masked text
#     trainer.train()

#     # Step 7: Save the trained model
#     model.save_pretrained("model_jarvis")

# if __name__ == "__main__":
#     main()
