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

// JavaScript to handle light/dark mode switching
function toggleTheme() {
    const body = document.body;
    const themeSwitcher = document.getElementById('themeSwitcher');

    // Toggle the theme class on body
    if (body.classList.contains('light-theme')) {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
        themeSwitcher.innerText = "Switch to Light Mode";
    } else {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
        themeSwitcher.innerText = "Switch to Dark Mode";
    }
}

// Function to load the theme from localStorage when the page loads
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const themeSwitcher = document.getElementById('themeSwitcher');

    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        themeSwitcher.innerText = "Switch to Light Mode";
    } else {
        body.classList.add('light-theme');
        themeSwitcher.innerText = "Switch to Dark Mode";
    }
}

// Run loadTheme() when the page is loaded to apply the stored theme
document.addEventListener("DOMContentLoaded", loadTheme);
