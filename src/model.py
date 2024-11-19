import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

def load_model_and_tokenizer():
    """
    Load the fine-tuned GPT-2 model and tokenizer.
    """
    model_path = os.path.join("model", "fine_tuned_gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, tokenizer, device
