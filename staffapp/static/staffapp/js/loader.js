const signInText = document.getElementsByClassName('birthday-cake');
const spinner = document.getElementsByClassName('spinner');
const submitButton = document.getElementById('submit-button');

submitButton.onclick = function(event) {
    signInText.style.display = "none";
    spinner.style.display = "block";
    // submitButton.disabled = true;
};