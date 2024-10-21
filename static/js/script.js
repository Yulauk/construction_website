function onSubmit(token) {
    // Call validateForm to check if the form is valid
    if (validateForm()) {
        // If the form is valid, submit it
        document.getElementById("consultationForm").submit();
    }
}

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
    if (!/^\+?\d{6,13}$/.test(phone)) {
        displayError("phone", "Invalid phone number. Please enter 6 to 13 digits, optionally starting with a plus sign.");
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



document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.portfolio_img').forEach(function (thumbnail, index) {
            thumbnail.addEventListener('click', function () {
                document.querySelectorAll('#carouselExampleControls .carousel-inner .carousel-item').forEach(function (item) {
                    item.classList.remove('active');
                });

                var carouselItem = document.querySelector('#carouselExampleControls .carousel-inner').children[index];
                carouselItem.classList.add('active');
            });
        });
    });

document.addEventListener('DOMContentLoaded', function () {
    // Select the form
    var form = document.getElementById('contactForm');

    // Add event listener to the form on submission
    form.addEventListener('submit', function (event) {
        // Check each field before submitting the form
        var isValid = true;

        // Validate Name (should not be empty)
        var nameInput = document.getElementById('validationContactName');
        var nameError = document.getElementById('nameError');

        if (!nameInput.value.trim() || nameInput.value.trim().length < 2 || /\d/.test(nameInput.value.trim())) {
            nameError.textContent = 'Invalid first name. Please enter at least two letters and no numbers.';
            isValid = false;
        } else {
            nameError.textContent = ''; // Clear any previous error message
        }

        // Validate Last Name (should not be empty)
        var lastNameInput = document.getElementById('validationContactLastName');
        var lastNameError = document.getElementById('lastNameError');

        if (!lastNameInput.value.trim()) {
            lastNameError.textContent = 'Please enter your last name.';
            isValid = false;
        } else {
            lastNameError.textContent = ''; // Clear any previous error message
        }

        // Validate Email (should match email format)
        var emailInput = document.getElementById('validationContactEmail');
        var emailError = document.getElementById('emailError');
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(emailInput.value.trim())) {
            emailError.textContent = 'Please enter a valid email address.';
            isValid = false;
        } else {
            emailError.textContent = ''; // Clear any previous error message
        }

        // Validate Phone (should contain only numbers)
        var phoneInput = document.getElementById('validationContactPhone');
        var phoneError = document.getElementById('phoneError');
        var phoneRegex = /^\d+$/;

        if (!phoneRegex.test(phoneInput.value.trim())) {
            phoneError.textContent = 'Please enter a valid phone number.';
            isValid = false;
        } else {
            phoneError.textContent = ''; // Clear any previous error message
        }

        // Validate City (should not be empty)
        var cityInput = document.getElementById('validationContactCity');
        var cityError = document.getElementById('cityError');
//if (!cityInput.value.trim() || cityInput.value.trim().length < 3 || /\d/.test(cityInput.value.trim())) {
//            nameError.textContent = 'Invalid first name. Please enter at least two letters and no numbers.';
//            isValid = false;
//        } else {
//            nameError.textContent = ''; // Clear any previous error message
//        }
        if (!cityInput.value.trim() || cityInput.value.trim().length < 3 || /\d/.test(cityInput.value.trim())) {
            cityError.textContent = 'Invalid city. Please enter at least three letters and no numbers.';
            isValid = false;
        } else {
            cityError.textContent = ''; // Clear any previous error message
        }

        // Validate State (optional, no specific validation)
        var stateInput = document.getElementById('validationContactState');

        // Validate Zip (optional, should contain only numbers)
        var zipInput = document.getElementById('validationContactZip');
        var zipError = document.getElementById('zipError');

        if (zipInput.value.trim() !== '' && !phoneRegex.test(zipInput.value.trim())) {
            zipError.textContent = 'Please enter a valid zip code or leave it empty.';
            isValid = false;
        } else {
            zipError.textContent = ''; // Clear any previous error message
        }

        // Validate Address (optional, no specific validation)
        var addressInput = document.getElementById('validationContactAddres');

        // Validate Budget (should not be the default value)
        var budgetSelect = document.getElementById('validationContactBudget');
        var budgetError = document.getElementById('budgetError');

        if (budgetSelect.value === '') {
            budgetError.textContent = 'Please select a budget range.';
            isValid = false;
        } else {
            budgetError.textContent = ''; // Clear any previous error message
        }

        // Validate Project Time (should not be the default value)
        var timeSelect = document.getElementById('validationContactTime');
        var timeError = document.getElementById('timeError');

        if (timeSelect.value === '') {
            timeError.textContent = 'Please select a project time frame.';
            isValid = false;
        } else {
            timeError.textContent = ''; // Clear any previous error message
        }

        // Validate How did you hear about us? (optional, no specific validation)
        var sourceSelect = document.getElementById('validationContactAbout');

        // Validate Project (should not be empty)
        var projectTextarea = document.getElementById('validationContactProject');
        var projectError = document.getElementById('projectError');

        if (!projectTextarea.value.trim()) {
            projectError.textContent = 'Please provide information about your project.';
            isValid = false;
        } else {
            projectError.textContent = ''; // Clear any previous error message
        }

        // If any validation fails, prevent form submission
        if (!isValid) {
            event.preventDefault();
        }
    });
});


//MODAL
// Wait for the DOM to fully load before attaching event listeners
document.addEventListener("DOMContentLoaded", function() {

    // Get the modal element
    var modal = document.getElementById("consultationModal");

    // Get all buttons with the class 'openModalButton'
    var buttons = document.querySelectorAll(".openModalButton");

    // Get the <span> element that closes the modal
    var span = document.getElementById("closeModal");

    // Loop through all buttons and add event listener to each
    buttons.forEach(function(btn) {
        btn.onclick = function(event) {
            event.preventDefault(); // Prevent default anchor behavior
            modal.style.display = "flex"; // Use 'flex' to center the modal
        }
    });

    // Close the modal when the user clicks on <span> (x)
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Close the modal if the user clicks outside the modal content
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});



document.addEventListener("DOMContentLoaded", function() {
    const dropdownButton = document.getElementById("languageDropdown");
    const dropdownMenu = document.getElementById("languageMenu");

    // Показать/скрыть меню при нажатии на кнопку
    dropdownButton.addEventListener("click", function(event) {
        event.stopPropagation(); // Остановить всплытие события
        dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });

    // Закрыть меню, если кликнули вне его
    window.addEventListener("click", function(event) {
        if (!event.target.closest('#index_header')) {
            dropdownMenu.style.display = "none"; // Скрыть меню
        }
    });
});



document.addEventListener("DOMContentLoaded", function() {
    const dropdownButton = document.getElementById("customDropdownButton");
    const dropdownMenu = document.getElementById("customDropdownMenu");

    // Показать/скрыть меню при нажатии на кнопку
    dropdownButton.addEventListener("click", function(event) {
        event.stopPropagation(); // Останавливает всплытие события
        dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });

    // Закрыть меню, если кликнули вне его
    window.addEventListener("click", function(event) {
        if (!event.target.closest('.custom-dropdown')) {
            dropdownMenu.style.display = "none"; // Скрыть меню
        }
    });
});


function goBack() {
            window.history.back();
        }