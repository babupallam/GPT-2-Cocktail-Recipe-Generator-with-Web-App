def generate_recipe(prompt, model, tokenizer, device, max_length=150):
    """
    Generate a recipe based on the user prompt.
    Args:
        prompt (str): User input to generate the recipe.
        model (transformers.GPT2LMHeadModel): The model used for generation.
        tokenizer (transformers.GPT2Tokenizer): The tokenizer used for encoding.
        device (torch.device): Device to run the model (CPU or GPU).
        max_length (int): Maximum length of the generated recipe.
    Returns:
        str: The generated recipe.
    """
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
