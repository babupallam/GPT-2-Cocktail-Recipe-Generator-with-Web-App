# utils/model.py

from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_model_and_tokenizer(model_path="../models/fine_tuned_gpt2"):
    """
    Load the fine-tuned GPT-2 model and tokenizer.
    Args:
        model_path (str): Path to the fine-tuned model directory.
    Returns:
        model: Loaded GPT-2 model.
        tokenizer: Loaded GPT-2 tokenizer.
    """
    model = GPT2LMHeadModel.from_pretrained(model_path)
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)

    # Set the pad token to eos token, since GPT-2 does not have a pad token
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer
