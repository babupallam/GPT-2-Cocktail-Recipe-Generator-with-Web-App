function showSpinner() {
    // Display the loading spinner when form is submitted
    document.getElementById('spinner').classList.remove('d-none');
}

function setExamplePrompt(promptText) {
    // Set the value of the textarea to the selected example prompt
    document.getElementById('prompt').value = promptText;
}

function showToast() {
    // Show the toast notification to indicate that the recipe was generated successfully
    let toastElement = new bootstrap.Toast(document.getElementById('toast'));
    toastElement.show();
}

function favoriteRecipe(index) {
    // Toggle favorite icon for the recipe
    const favoriteIcon = document.querySelectorAll('.recipe-actions .material-icons')[index - 1];
    if (favoriteIcon.innerText === "favorite_border") {
        favoriteIcon.innerText = "favorite";
        favoriteIcon.classList.add("text-danger");
    } else {
        favoriteIcon.innerText = "favorite_border";
        favoriteIcon.classList.remove("text-danger");
    }
}

function editRecipe(index) {
    // Functionality to handle editing a recipe (currently just showing an alert)
    alert(`Editing recipe ${index} functionality is under construction.`);
}

function deleteRecipe(index) {
    // Functionality to handle deleting a recipe (currently just showing an alert)
    alert(`Deleting recipe ${index} functionality is under construction.`);
}
