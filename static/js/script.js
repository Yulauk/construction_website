function validateForm() {
    // Reset previous error messages
    resetErrorMessages();

    var username = document.getElementById("username").value;
    var phone = document.getElementById("phone").value;
    var comment = document.getElementById("comment").value;

    var isValid = true;

    // Validate username
    if (username.length < 2 || /\d/.test(username)) {
        displayError("username", "Invalid username. Please enter at least two letters and no numbers.");
        isValid = false;
    }

    // Validate phone number
    if (!/^\d{10}$/.test(phone)) {
        displayError("phone", "Invalid phone number. Please enter 10 digits.");
        isValid = false;
    }

    // Validate comment
    if (comment.length > 1000) {
        displayError("comment", "Comment is too long. Please limit it to 1000 characters.");
        isValid = false;
    }

    return isValid;
}

function resetErrorMessages() {
    document.getElementById("username-error").innerHTML = "";
    document.getElementById("phone-error").innerHTML = "";
    document.getElementById("comment-error").innerHTML = "";
}

function displayError(field, message) {
    document.getElementById(field + "-error").innerHTML = message;
}
