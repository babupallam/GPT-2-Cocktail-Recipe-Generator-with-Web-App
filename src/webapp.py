from flask import Flask, render_template, request, redirect, url_for
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

app = Flask(__name__)

# Load the fine-tuned model and tokenizer
model_path = os.path.join("model", "fine_tuned_gpt2")
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def generate_recipe(prompt, max_length=150):
    # Generate a recipe based on the user prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
    attention_mask = (input_ids != tokenizer.pad_token_id).long().to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        do_sample=True,
        repetition_penalty=2.0,
        pad_token_id=tokenizer.pad_token_id
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    generated_recipe = None
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            generated_recipe = generate_recipe(prompt)

    return render_template('index.html', generated_recipe=generated_recipe)


if __name__ == '__main__':
    app.run(debug=True)
