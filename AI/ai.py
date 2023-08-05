import torch
from transformers import (
    DistilBertTokenizer,
    DistilBertForQuestionAnswering,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset


def main():
    # Load the SQuAD dataset
    dataset = load_dataset("squad")

    # Load the pre-trained DistilBERT tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")
    model = DistilBertForQuestionAnswering.from_pretrained("distilbert-base-cased")

    # Preprocess the data and create datasets
    def preprocess_function(examples):
        return tokenizer(
            examples["question"],
            examples["context"],
            truncation=True,
            padding="max_length",
            max_length=384,
            return_overflowing_tokens=True,
        )

    train_dataset = dataset["train"].map(preprocess_function, batched=True)
    eval_dataset = dataset["validation"].map(preprocess_function, batched=True)

    # Set up the Trainer with appropriate training arguments
    training_args = TrainingArguments(
        output_dir="./squad_qa",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=100,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=lambda features: {
            "input_ids": torch.stack([f for f in features["input_ids"]]),
            "attention_mask": torch.stack([f for f in features["attention_mask"]]),
            "start_positions": torch.stack([f for f in features["start_positions"]]),
            "end_positions": torch.stack([f for f in features["end_positions"]]),
        },
    )

    # Start the training
    trainer.train()

    # Save the model after training
    trainer.save_model()


if __name__ == "__main__":
    main()
