from flask import Flask, render_template, request
from model import load_model_and_tokenizer
from generator import generate_recipe

# Create Flask app
app = Flask(__name__, template_folder='../webapp/templates', static_folder='../webapp/static')

# Load model, tokenizer, and set device
model, tokenizer, device = load_model_and_tokenizer()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the '/' route.
    Render the main page where users can input prompts to generate a recipe.
    """
    generated_recipe = None
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            generated_recipe = generate_recipe(prompt, model, tokenizer, device)

    return render_template('index.html', generated_recipe=generated_recipe)


if __name__ == '__main__':
    app.run(debug=True)
