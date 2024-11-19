import re

# Sample List of Generated Recipes from the Model
# (In practice, this would be the output from the generate_recipes function.)
recipes = [
    """Create a detailed fruit cocktail recipe using pineapple and mint. The recipe should have two parts:
    - Ingredients: List all the ingredients needed.
    - Instructions: Describe how to prepare the cocktail step by step.

    Ingredients:
    - 1 cup fresh pineapple juice
    - 1/4 cup fresh mint leaves
    - 1 tablespoon honey
    - Ice cubes

    Instructions:
    1. Combine pineapple juice, mint leaves, and honey in a blender.
    2. Blend until smooth.
    3. Pour into a glass with ice cubes and garnish with a mint sprig.""",
    # Add other generated recipes here...
]


# Define the Post-Processing Function
def post_process_recipe(output):
    """
    Post-process the generated recipe to ensure it includes both Ingredients and Instructions.
    Args:
        output (str): The generated text.
    Returns:
        str: The processed recipe with proper formatting.
    """
    # Extract ingredients and instructions using regex
    ingredients_match = re.findall(r"Ingredients:(.*?)(Instructions:|$)", output, re.DOTALL)
    instructions_match = re.findall(r"Instructions:(.*)", output, re.DOTALL)

    # Clean up the ingredients and instructions
    ingredients_text = ingredients_match[0][
        0].strip() if ingredients_match else "Ingredients not found. Please add a list of ingredients."
    instructions_text = instructions_match[
        0].strip() if instructions_match else "Instructions not found. Please add preparation steps."

    # Reformat the output to ensure readability
    return f"Ingredients:\n{ingredients_text}\n\nInstructions:\n{instructions_text}"


# Loop Through Generated Recipes and Process Them
for i, recipe in enumerate(recipes, start=1):
    processed_recipe = post_process_recipe(recipe)
    print(f"\nProcessed Recipe {i}:\n{processed_recipe}\n{'=' * 80}\n")
