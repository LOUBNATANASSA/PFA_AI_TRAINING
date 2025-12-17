// Progress tracking
const totalQuestions = 15;
let currentQuestion = 1;

// Store answers in a dictionary
let answers = {};

// Update progress bar
function updateProgress(questionNumber) {
  const progressPercentage = ((questionNumber - 1) / (totalQuestions - 1)) * 100;
  document.getElementById('progressFill').style.width = progressPercentage + '%';

  // Update circle status
  for (let i = 1; i <= totalQuestions; i++) {
    const circle = document.getElementById('circle' + i);
    if (i <= questionNumber) {
      circle.classList.add('active');
    } else {
      circle.classList.remove('active');
    }
  }
}

// Show error message
function showErrorMessage() {
  const errorMessage = document.getElementById('errorMessage');
  errorMessage.classList.remove('hidden');
}

// Hide error message
function hideErrorMessage() {
  document.getElementById('errorMessage').classList.add('hidden');
}

// Validate current question and store answers
function validateQuestion(questionElement) {
  const inputs = questionElement.querySelectorAll('input[required], select[required]');
  let isValid = true;

  inputs.forEach(input => {
    let answer;
    if (input.type === 'radio') {
      const name = input.name;
      const radioGroup = document.querySelectorAll(`input[name="${name}"]:checked`);
      if (radioGroup.length === 0) {
        isValid = false;
      } else {
        answer = radioGroup[0].value; // Store the selected answer
        answers[name] = answer; // Store answer in the dictionary
        // Log the answer
      }
    } else if (input.type === 'text' || input.type === 'select-one') {
      if (!input.value) {
        isValid = false;
      } else {
        answer = input.value; // Store the input value
        answers[input.name] = answer; // Store answer in the dictionary
        // Log the answer
      }
    }
  });

  return isValid;
}

// Go to next question with conditional logic
function nextQuestion(current) {
  const currentQuestionElement = document.getElementById('question' + current);

  // Validate the current question
  if (!validateQuestion(currentQuestionElement)) {
    showErrorMessage();
    return;
  }

  hideErrorMessage();
  currentQuestionElement.classList.remove('active');

  let nextQuestionNumber = current + 1; // Default next question

  // Conditional logic for question 5 (lipid test)
  if (current === 5) {
    const lipidTestValue = document.querySelector('input[name="lipidTest"]:checked').value;
    if (lipidTestValue === 'no') {
      nextQuestionNumber = 7; // Skip LDL level question if no lipid test
    }
    // If 'yes', proceed to question 6 (default behavior)
  }

  const nextQuestionElement = document.getElementById('question' + nextQuestionNumber);

  if (nextQuestionElement) {
    nextQuestionElement.classList.add('active');
    currentQuestion = nextQuestionNumber;
    updateProgress(currentQuestion);
  }
}

// Go to previous question with conditional logic
function prevQuestion(current) {
  const currentQuestionElement = document.getElementById('question' + current);
  currentQuestionElement.classList.remove('active');

  let prevQuestionNumber = current - 1; // Default previous question

  // Special handling for going back from question 7
  if (current === 7) {
    // Check if user came directly from question 5 (skipped 6)
    const lipidTestValue = document.querySelector('input[name="lipidTest"]:checked');
    if (lipidTestValue && lipidTestValue.value === 'no') {
      prevQuestionNumber = 5;
    }
    // Otherwise, the default (question 6) is correct
  }

  const prevQuestionElement = document.getElementById('question' + prevQuestionNumber);

  if (prevQuestionElement) {
    prevQuestionElement.classList.add('active');
    currentQuestion = prevQuestionNumber;
    updateProgress(currentQuestion);
  }

  hideErrorMessage();
}

// Handle radio option selection styling
document.querySelectorAll('.radio-option').forEach(option => {
  option.addEventListener('click', function () {
    const name = this.querySelector('input').name;
    document.querySelectorAll(`input[name="${name}"]`).forEach(input => {
      input.closest('.radio-option').classList.remove('selected');
    });
    this.classList.add('selected');
    this.querySelector('input').checked = true;

    // Hide error message when an option is selected
    hideErrorMessage();
  });
});

// Add event listeners to selects
document.querySelectorAll('select[required]').forEach(select => {
  select.addEventListener('change', function () {
    if (this.value) {
      hideErrorMessage();
    }
  });
});

// Handle form submission - for the final question
document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.querySelector('.submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', function (event) {
      const currentQuestionElement = document.getElementById('question' + currentQuestion);

      // Validate the final question
      if (!validateQuestion(currentQuestionElement)) {
        event.preventDefault();
        showErrorMessage();
      } else {
        // If valid, log all answers

        // Display the collected answers
      }
    });
  }
});

// Initialize
updateProgress(1);


// Handle form submission - for the final question
document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.querySelector('.submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', function (event) {
      const currentQuestionElement = document.getElementById('question' + currentQuestion);

      // Validate the final question
      if (!validateQuestion(currentQuestionElement)) {
        event.preventDefault();
        showErrorMessage();
      } else {
        alert("Attempting to save results..."); // DEBUG ALERT
        // Désactiver le bouton pendant l'envoi
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Enregistrement...';

        // Envoi des réponses au backend Django
        const token = getCookie('csrftoken');
        fetch('/Cholesterol-results/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
          },
          credentials: 'include', // FORCE COOKIES
          body: JSON.stringify({ responses: answers })
        })
          .then(response => {
            if (response.status === 401 || response.status === 403) {
              alert('Veuillez vous connecter pour enregistrer vos résultats.');
              window.location.href = '/login/';
              return;
            }
            return response.json();
          })
          .then(data => {
            if (data && data.status === 'success') {
              alert('Test enregistré avec succès !');
              window.location.href = '/historique/';
            } else if (data && data.message) {
              alert('Erreur: ' + data.message);
              submitBtn.disabled = false;
              submitBtn.innerHTML = 'Finish';
            }
          })
          .catch(error => {
            console.error('Erreur:', error);
            alert('Une erreur est survenue (Network/JS): ' + error);
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Finish';
          });
      }
    });
  }
});

// Fonction pour obtenir le token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
