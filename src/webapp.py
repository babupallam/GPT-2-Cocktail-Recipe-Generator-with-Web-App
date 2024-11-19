from flask import Flask, render_template, request, session
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from generator import generate_recipe

# Create Flask app
app = Flask(__name__, template_folder='../webapp/templates', static_folder='../webapp/static')
app.secret_key = 'your_secret_key_here'  # Required for session management


# Load model and tokenizer globally so they do not load every time the page is refreshed.
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

@app.route("/", methods=["GET", "POST"])
def index():
    generated_recipe = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        input_ids = tokenizer.encode(user_input, return_tensors="pt")

        # Generate the recipe
        output = model.generate(
            input_ids,
            max_length=150,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode and get the generated recipe
        generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)

        # Save generated recipe to session history
        if "recipe_history" not in session:
            session["recipe_history"] = []
        session["recipe_history"].append(generated_recipe)
        session.modified = True

    # Fetch the recipe history from session
    recipe_history = session.get("recipe_history", [])
    return render_template("index.html", generated_recipe=generated_recipe, recipe_history=recipe_history)

if __name__ == "__main__":
    app.run(debug=True)
