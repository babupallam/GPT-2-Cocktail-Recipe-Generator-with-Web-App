import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Define paths for the saved model and tokenizer
MODEL_OUTPUT_DIR = os.path.join("model", "fine_tuned_gpt2")

# Step 1: Load the Fine-Tuned Model and Tokenizer
def load_fine_tuned_model(model_output_dir):
    """
    Load the fine-tuned model and tokenizer from disk.
    Args:
        model_output_dir (str): Directory where the fine-tuned model and tokenizer are saved.
    Returns:
        Tuple: Loaded model and tokenizer.
    """
    print(f"Loading the fine-tuned model and tokenizer from {model_output_dir}...")
    model = GPT2LMHeadModel.from_pretrained(model_output_dir)
    tokenizer = GPT2Tokenizer.from_pretrained(model_output_dir)

    # Add a distinct pad token if it does not exist
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))

    model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    return model, tokenizer


# Step 2: Define Predefined Prompts for Testing
# Step 2: Define Predefined Prompts for Testing
def get_test_prompts():
    """
    Returns a list of predefined prompts for testing the model.
    Each prompt includes explicit instructions for Ingredients and Instructions.
    """
    return [
        "Create a detailed fruit cocktail recipe using pineapple and mint. The recipe should have two parts:\n"
        "- Ingredients: Provide a detailed list of ingredients required.\n"
        "- Instructions: Write clear step-by-step preparation instructions for the fruit cocktail.",

        "Write a detailed fruit cocktail recipe using mango and orange. The recipe must include two parts:\n"
        "- Ingredients: List all the ingredients needed.\n"
        "- Instructions: Describe how to prepare the cocktail step by step.",

        "Provide a recipe for a strawberry and basil summer fruit cocktail. Include the following:\n"
        "- Ingredients: A complete list of ingredients.\n"
        "- Instructions: Step-by-step preparation process.",

        "Generate a tropical fruit cocktail recipe with coconut and pineapple. The recipe should have these sections:\n"
        "- Ingredients: Mention all the ingredients required.\n"
        "- Instructions: Describe the process to prepare the cocktail.",

        "Create a winter-themed fruit cocktail recipe with cranberries and cinnamon. The recipe should contain:\n"
        "- Ingredients: A list of all ingredients.\n"
        "- Instructions: Clear instructions on how to prepare the cocktail."
    ]


# Step 3: Generate Recipes Based on the Prompts
def generate_recipes(model, tokenizer, prompts, max_length=150):
    """
    Generate fruit cocktail recipes based on the predefined prompts.
    Args:
        model (GPT2LMHeadModel): The fine-tuned model.
        tokenizer (GPT2Tokenizer): The tokenizer.
        prompts (list): List of prompts for generating recipes.
        max_length (int): Maximum length of the generated text.
    Returns:
        list: Generated recipes.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    generated_recipes = []
    for prompt in prompts:
        # Tokenize the input prompt and create attention mask
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        attention_mask = (input_ids != tokenizer.pad_token_id).long().to(device)

        # Generate text using the model with attention mask
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,  # Include the attention mask for more reliable results
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.7,
            pad_token_id=tokenizer.pad_token_id  # Use the pad token properly
        )

        # Decode the generated text
        generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_recipes.append(generated_recipe)

    return generated_recipes


# Step 4: Print and Evaluate the Generated Recipes
def evaluate_generated_recipes(recipes):
    """
    Print out the generated recipes for evaluation.
    Args:
        recipes (list): List of generated recipes.
    """
    print("\nGenerated Recipes:")
    for idx, recipe in enumerate(recipes, start=1):
        print(f"\nGenerated Recipe {idx}:")
        print(recipe)
        print("\n" + "=" * 80)


# Step 5: Main function to run the test
def main():
    # Step 5.1: Load the Fine-Tuned Model and Tokenizer
    model, tokenizer = load_fine_tuned_model(MODEL_OUTPUT_DIR)

    # Step 5.2: Get Test Prompts
    test_prompts = get_test_prompts()

    # Step 5.3: Generate Recipes
    generated_recipes = generate_recipes(model, tokenizer, test_prompts)

    # Step 5.4: Evaluate Generated Recipes
    evaluate_generated_recipes(generated_recipes)


if __name__ == "__main__":
    main()
