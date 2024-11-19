import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os


# Load the Fine-Tuned Model and Tokenizer
MODEL_OUTPUT_DIR = os.path.join("model", "fine_tuned_gpt2")


model = GPT2LMHeadModel.from_pretrained(MODEL_OUTPUT_DIR)
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_OUTPUT_DIR)

model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))


# Define Prompts for Testing
def get_test_prompts():
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
    ]


# Generate Recipes
def generate_recipes(model, tokenizer, prompts, max_length=150):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    generated_recipes = []
    for prompt in prompts:
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        attention_mask = (input_ids != tokenizer.pad_token_id).long().to(device)

        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.7,
            pad_token_id=tokenizer.pad_token_id
        )

        generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_recipes.append(generated_recipe)

    return generated_recipes


# Run Recipe Generation
prompts = get_test_prompts()
recipes = generate_recipes(model, tokenizer, prompts)

# Print Recipes
for i, recipe in enumerate(recipes, start=1):
    print(f"\nGenerated Recipe {i}:\n{recipe}\n{'=' * 80}\n")
