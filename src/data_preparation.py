import os
from datasets import load_dataset
from transformers import GPT2Tokenizer

# Define constants for dataset paths
DATASET_CSV_PATH = os.path.join("data", "RecipeNLG_dataset.csv")
TOKENIZED_DATA_DIR = os.path.join("data", "tokenized_data")


def load_dataset_from_csv(dataset_csv_path):
    """
    Load dataset from a local CSV file using Hugging Face's load_dataset.
    Args:
        dataset_csv_path (str): Path to the CSV file.
    Returns:
        Dataset: Loaded dataset.
    """
    if not os.path.exists(dataset_csv_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_csv_path}. Please ensure the CSV file is present.")
    print(f"Loading dataset from {dataset_csv_path}...")
    dataset = load_dataset('csv', data_files=dataset_csv_path, split='train')
    print(f"Loaded dataset columns: {dataset.column_names}")
    return dataset


def split_dataset(dataset, test_size=0.2, seed=42):
    """
    Split the dataset into training and evaluation datasets.
    Args:
        dataset (Dataset): The dataset to be split.
        test_size (float): Proportion of the dataset to include in the test split.
        seed (int): Random seed for reproducibility.
    Returns:
        Tuple[Dataset, Dataset]: Training and evaluation datasets.
    """
    print("Splitting dataset into training and evaluation sets...")
    split_dataset = dataset.train_test_split(test_size=test_size, seed=seed)
    train_dataset = split_dataset['train']
    eval_dataset = split_dataset['test']
    return train_dataset, eval_dataset


def load_and_prepare_tokenizer():
    """
    Load GPT-2 tokenizer and add special tokens.
    Returns:
        GPT2Tokenizer: Tokenizer with added special tokens.
    """
    print("Loading GPT-2 tokenizer and adding special tokens...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    return tokenizer


def preprocess_text_column(dataset, text_column):
    """
    Preprocess the text column to ensure all data is properly formatted as strings.
    Args:
        dataset (Dataset): Dataset to preprocess.
        text_column (str): The column to process.
    Returns:
        Dataset: Cleaned dataset.
    """
    print("Preprocessing text column to ensure correct format...")

    def clean_text(examples):
        # Convert all entries to strings, replacing None with an empty string
        cleaned_text = [str(text) if text is not None else "" for text in examples[text_column]]
        return {text_column: cleaned_text}

    return dataset.map(clean_text, batched=True)


def tokenize_dataset(dataset, tokenizer, text_column, max_length=128):
    """
    Tokenize a dataset using the provided tokenizer.
    Args:
        dataset (Dataset): Dataset to tokenize.
        tokenizer (GPT2Tokenizer): Tokenizer to use.
        text_column (str): The column to tokenize.
        max_length (int): Maximum length for tokenization.
    Returns:
        Dataset: Tokenized dataset.
    """
    print("Tokenizing dataset...")

    def tokenize_function(examples):
        # Extract the text column as a list of strings for the tokenizer
        texts = examples[text_column]
        # Ensure all entries are strings
        texts = [str(text) for text in texts]
        return tokenizer(texts, truncation=True, padding='max_length', max_length=max_length)

    return dataset.map(tokenize_function, batched=True)


def save_tokenized_datasets(train_dataset, eval_dataset, output_dir):
    """
    Save tokenized training and evaluation datasets to disk.
    Args:
        train_dataset (Dataset): Tokenized training dataset.
        eval_dataset (Dataset): Tokenized evaluation dataset.
        output_dir (str): Directory where datasets should be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving tokenized training dataset to {os.path.join(output_dir, 'tokenized_train')}...")
    train_dataset.save_to_disk(os.path.join(output_dir, "tokenized_train"))
    print(f"Saving tokenized evaluation dataset to {os.path.join(output_dir, 'tokenized_eval')}...")
    eval_dataset.save_to_disk(os.path.join(output_dir, "tokenized_eval"))
    print("Tokenized datasets saved successfully.")


def main():
    # Step 1: Load Dataset from CSV
    dataset = load_dataset_from_csv(DATASET_CSV_PATH)

    # Step 2: Split Dataset into Training and Evaluation Sets
    train_dataset, eval_dataset = split_dataset(dataset)

    # Step 3: Load Tokenizer
    tokenizer = load_and_prepare_tokenizer()

    # Step 4: Preprocess the Text Column
    text_column = dataset.column_names[0]  # Assuming the text column is the first one; update if different
    train_dataset = preprocess_text_column(train_dataset, text_column)
    eval_dataset = preprocess_text_column(eval_dataset, text_column)

    # Step 5: Tokenize Datasets
    tokenized_train_dataset = tokenize_dataset(train_dataset, tokenizer, text_column)
    tokenized_eval_dataset = tokenize_dataset(eval_dataset, tokenizer, text_column)

    # Step 6: Save Tokenized Datasets
    save_tokenized_datasets(tokenized_train_dataset, tokenized_eval_dataset, TOKENIZED_DATA_DIR)

    print("Data preparation process completed successfully.")


if __name__ == "__main__":
    main()
