# utils/generator.py

import torch

def generate_recipe(prompt, model, tokenizer, max_length=250):
    """
    Generate a fruit cocktail recipe using the provided prompt.
    Args:
        prompt (str): User input to generate the recipe.
        model: Pre-trained or fine-tuned model to generate text.
        tokenizer: Tokenizer associated with the model.
        max_length (int): The maximum length for the generated output.
    Returns:
        str: Generated recipe text.
    """
    # Construct the structured prompt
    structured_prompt = (
        f" The recipe should have two parts:\n"
        "- Ingredients: Provide a detailed list of ingredients required.\n"
        "- Instructions: Write clear step-by-step preparation instructions for the fruit cocktail."
    )

    # Tokenize the input prompt
    input_ids = tokenizer.encode(structured_prompt, return_tensors='pt')

    # Generate attention mask based on the input IDs
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    # Generate text using the model with the attention mask
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

    # Decode the generated output
    generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_recipe
