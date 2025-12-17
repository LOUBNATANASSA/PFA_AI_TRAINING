//objet pour stocker les reponses
let userResponses = {};

// Progress tracking
const totalQuestions = 15;
let currentQuestion = 1;



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

// Validate current question
function validateQuestion(questionElement) {
  const inputs = questionElement.querySelectorAll('input[required], select[required]');
  let isValid = true;

  inputs.forEach(input => {
    if (input.type === 'radio') {
      const name = input.name;
      const radioGroup = document.querySelectorAll(`input[name="${name}"]:checked`);
      if (radioGroup.length === 0) {
        isValid = false;
      }
    } else if (!input.value) {
      isValid = false;
    }
  });

  return isValid;
}

// Go to next question with conditional logic
function nextQuestion(current) {
  const currentQuestionElement = document.getElementById('question' + current);

  // Valider la question actuelle
  if (!validateQuestion(currentQuestionElement)) {
    showErrorMessage();
    return;
  }

  hideErrorMessage();

  // Sauvegarder la réponse
  saveUserResponse(current);

  currentQuestionElement.classList.remove('active');
  let nextQuestionNumber = current + 1;

  // Logique conditionnelle
  if (current === 2) {
    const bothParentsValue = document.querySelector('input[name="bothparents"]:checked').value;
    if (bothParentsValue === 'yes') {
      nextQuestionNumber = 4;
    }
  } else if (current === 10) {
    const hemoglobinTestValue = document.querySelector('input[name="hemoglobinTest"]:checked').value;
    if (hemoglobinTestValue === 'no') {
      nextQuestionNumber = 12;
    }
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

  // Special handling for going back from question 4
  if (current === 4) {
    // Check if user came directly from question 2 (skipped 3)
    const bothParentsValue = document.querySelector('input[name="bothparents"]:checked');
    if (bothParentsValue && bothParentsValue.value === 'yes') {
      prevQuestionNumber = 2;
    }
    // Otherwise, the default (question 3) is correct
  }


  // Special handling for going back from question 12
  else if (current === 12) {
    // Check if user came from question 10 (skipped 11)
    const hemoglobinTestValue = document.querySelector('input[name="hemoglobinTest"]:checked');
    if (hemoglobinTestValue && hemoglobinTestValue.value === 'no') {
      prevQuestionNumber = 10;
    }
    // Otherwise, the default (question 11) is correct
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
      }
    });
  }
});

// Initialize
updateProgress(1);

function saveUserResponse(questionNumber) {

  const questionElement = document.getElementById('question' + questionNumber);
  const inputs = questionElement.querySelectorAll('input, select');

  inputs.forEach(input => {
    if (input.type === 'radio' && input.checked) {
      userResponses[input.name] = input.value;
    } else if (input.tagName === 'SELECT' && input.value) {
      userResponses[input.name] = input.value;
    }
  });

  // Vérification des réponses en console
}

function submitResponses() {
  alert("Attempting to save results..."); // DEBUG ALERT
  saveUserResponse(15);

  // Afficher un indicateur de chargement
  submitBtn.innerHTML = 'Enregistrement...';
}

const token = getCSRFToken();
// alert("Token found: " + token); // DEBUG

fetch('/save-result/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': token
  },
  credentials: 'include', // FORCE COOKIES
  body: JSON.stringify(userResponses)
})
  .then(response => {
    // alert("Response status: " + response.status); // DEBUG
    if (response.status === 401 || response.status === 403) {
      alert('Veuillez vous connecter pour enregistrer vos résultats.');
      window.location.href = '/login/';
      return;
    }
    return response.json();
  })
  .then(data => {
    if (data && (data.message || data.id)) {
      alert('Test enregistré avec succès !');
      window.location.href = '/historique/';
    } else if (data && data.error) {
      alert('Erreur: ' + data.error);
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Finish';
      }
    }
  })
  .catch(error => {
    console.error('Erreur:', error);
    alert('Une erreur est survenue (Network/JS): ' + error);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Finish';
    }
  });
}

// Fonction pour récupérer le token CSRF
function getCSRFToken() {
  return document.cookie.split('; ')
    .find(row => row.startsWith('csrftoken'))
    ?.split('=')[1] || '';
}




