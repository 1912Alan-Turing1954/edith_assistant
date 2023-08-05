import torch
from transformers import GPT2Tokenizer, GPT2ForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset

# Load SQuAD dataset
dataset = load_dataset("squad")

# Filter out examples that do not have start_positions
def filter_examples(example):
    return 'start_positions' in example

dataset = dataset.map(filter_examples, num_proc=4)

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2ForQuestionAnswering.from_pretrained("gpt2")

# Tokenize the filtered dataset
def tokenize_function(examples):
    return tokenizer(examples["question"], examples["context"], truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Training settings
training_args = TrainingArguments(
    output_dir="./output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=1000,
    save_total_limit=2,
    prediction_loss_only=True,
    disable_tqdm=True,  # Disable tqdm progress bar
    report_to="none",   # Disable Wandb logging
)

# Data collator function
def data_collator(batch):
    return {
        'input_ids': torch.stack([example['input_ids'] for example in batch]),
        'attention_mask': torch.stack([example['attention_mask'] for example in batch]),
        'start_positions': torch.stack([example['start_positions'] for example in batch]),
        'end_positions': torch.stack([example['end_positions'] for example in batch]),
    }

# Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    data_collator=data_collator,
)

# Training loop
trainer.train()

# Save the model after fine-tuning
trainer.save_model("AI/model/gpt2_squad_finetuned_model")
