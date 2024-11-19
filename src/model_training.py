import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_from_disk

# Define constants for paths
TOKENIZED_DATA_DIR = os.path.join("data", "tokenized_data")
MODEL_OUTPUT_DIR = os.path.join("model", "fine_tuned_gpt2")

# Step 1: Load Tokenized Datasets from Google Drive
def load_datasets(tokenized_data_dir):
    print("Loading tokenized datasets from Google Drive...")
    tokenized_train_dataset = load_from_disk(os.path.join(tokenized_data_dir, "tokenized_train"))
    tokenized_eval_dataset = load_from_disk(os.path.join(tokenized_data_dir, "tokenized_eval"))
    return tokenized_train_dataset, tokenized_eval_dataset

# Step 2: Load Pre-trained Model and Tokenizer
def load_model_and_tokenizer():
    print("Loading pre-trained GPT-2 model and tokenizer...")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))
    model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    return model, tokenizer

# Step 3: Configure Training Arguments for Faster Evaluation
def configure_training_arguments(output_dir, epochs=0.0001, batch_size=8, eval_steps=500):
    """
    Configure training arguments for faster evaluation.
    Args:
        output_dir (str): Directory to save the trained model.
        epochs (int): Number of training epochs.
        batch_size (int): Batch size for training.
        eval_steps (int): Number of steps between evaluations to reduce frequency.
    Returns:
        TrainingArguments: Configured training arguments.
    """
    print("Configuring training arguments...")
    return TrainingArguments(
        output_dir=output_dir,
        # evaluation_strategy="epoch",  # Original: Evaluate after every epoch
        evaluation_strategy="steps",  # Debugging: Evaluate after a number of steps for simplification
        eval_steps=eval_steps,  # Debugging: Increase eval_steps to evaluate less frequently
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none"  # Disable logging to external services
    )

# Step 4: Train the Model with Modified Evaluation
def train_model(model, tokenizer, train_dataset, eval_dataset, training_args):
    print("Initializing Trainer and starting training...")

    # Use Hugging Face's DataCollatorForLanguageModeling for proper collation
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Set mlm to False for causal language modeling
    )

    # Original: Use full evaluation dataset
    # eval_dataset_to_use = eval_dataset

    # Debugging: Use only a subset of the evaluation dataset for quicker evaluation
    eval_dataset_to_use = eval_dataset.select(range(min(1000, len(eval_dataset))))  # Debugging: Use a smaller subset for evaluation

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset_to_use,  # Use either the full or a smaller evaluation set
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    # Original: Train with full dataset and standard evaluation
    # trainer.train()

    # Debugging: Train with modified evaluation settings to reduce evaluation time
    trainer.train()

# Step 5: Save the Fine-Tuned Model
def save_model(model, tokenizer, output_dir):
    print(f"Saving the fine-tuned model to Google Drive at {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Model and tokenizer saved successfully.")

# Step 6: Main function to orchestrate the whole process
def main():
    # Load Tokenized Datasets
    train_dataset, eval_dataset = load_datasets(TOKENIZED_DATA_DIR)

    # Load Pre-trained Model and Tokenizer
    model, tokenizer = load_model_and_tokenizer()

    # Configure Training Arguments with Faster Evaluation
    training_args = configure_training_arguments(MODEL_OUTPUT_DIR, eval_steps=1000)

    # Train the Model with Modified Evaluation Strategy
    train_model(model, tokenizer, train_dataset, eval_dataset, training_args)

    # Save the Fine-Tuned Model
    save_model(model, tokenizer, MODEL_OUTPUT_DIR)

    print("Model training and saving completed successfully.")

if __name__ == "__main__":
    main()
