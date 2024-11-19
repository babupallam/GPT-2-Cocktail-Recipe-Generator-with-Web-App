from flask import Flask, render_template, request, session
from model import load_model_and_tokenizer
from generator import generate_recipe

# Create Flask app
app = Flask(__name__, template_folder='../webapp/templates', static_folder='../webapp/static')
app.secret_key = 'your_secret_key_here'  # Required for session management

# Load model, tokenizer, and set device
model, tokenizer, device = load_model_and_tokenizer()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the '/' route.
    Render the main page where users can input prompts to generate a recipe.
    Display the history of generated recipes as well.
    """
    generated_recipe = None

    # If session does not have a 'history', initialize it
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            generated_recipe = generate_recipe(prompt, model, tokenizer, device)

            # Add generated recipe to the history list in the session
            history = session.get('history')
            history.append(generated_recipe)

            # Update session explicitly
            session['history'] = history
            session.modified = True  # Mark session as modified to ensure it saves the changes

    # Get recipe history from session
    recipe_history = session.get('history')

    return render_template('index.html', generated_recipe=generated_recipe, recipe_history=recipe_history)

if __name__ == '__main__':
    app.run(debug=True)
