# webapp.py

from flask import Flask, render_template, request, redirect, url_for
from model import load_model_and_tokenizer
from generator import generate_recipe

# Initialize Flask app
app = Flask(__name__)

# Load the fine-tuned model and tokenizer
model_path = "/models/fine_tuned_gpt2"
model, tokenizer = load_model_and_tokenizer(model_path)


# Define a route for the homepage
@app.route('/', methods=["GET", "POST"])
def index():
    generated_recipe = None
    if request.method == "POST":
        prompt = request.form["prompt"]

        # Generate the recipe using the fine-tuned model
        generated_recipe = generate_recipe(prompt, model, tokenizer)

    # Render the index page, passing the generated recipe if it exists
    return render_template('index.html', generated_recipe=generated_recipe)


# Function for setting example prompt via a URL route
@app.route('/set_prompt/<example>', methods=["GET"])
def set_prompt(example):
    return redirect(url_for('index', prompt=example))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
