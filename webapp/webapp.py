# app/webapp.py

from flask import Flask, render_template, request, redirect, url_for
from utils.model import load_model_and_tokenizer
from utils.generator import generate_recipe

# Initialize Flask app
app = Flask(__name__)

# Load the fine-tuned model and tokenizer
model_path = "model/fine_tuned_gpt2"
model, tokenizer = load_model_and_tokenizer(model_path)

# In-memory storage for recipe history
recipe_history = []


# Define a route for the homepage
@app.route('/', methods=["GET", "POST"])
def index():
    generated_recipe = None
    if request.method == "POST":
        prompt = request.form["prompt"]

        # Generate the recipe using the fine-tuned model
        generated_recipe = generate_recipe(prompt, model, tokenizer)

        # Store the generated recipe in history
        recipe_history.append({
            'prompt': prompt,
            'recipe': generated_recipe
        })

    # Render the index page, passing the generated recipe and recipe history
    return render_template('index.html', generated_recipe=generated_recipe, recipe_history=recipe_history)


# Function for setting example prompt via a URL route
@app.route('/set_prompt/<example>', methods=["GET"])
def set_prompt(example):
    return redirect(url_for('index', prompt=example))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
