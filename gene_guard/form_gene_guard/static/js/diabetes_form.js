let total = 8;

function nextQuestion(n) {
  document.getElementById(`q${n}`).classList.remove('active');
  document.getElementById(`q${n+1}`).classList.add('active');
  updateProgress(n + 1);
}
function prevQuestion(n) {
  document.getElementById(`q${n}`).classList.remove('active');
  document.getElementById(`q${n-1}`).classList.add('active');
  updateProgress(n - 1);
}
function updateProgress(step) {
  const fill = document.getElementById("progressFill");
  const percent = ((step - 1) / (total - 1)) * 100;
  fill.style.width = percent + "%";
  for (let i = 1; i <= total; i++) {
    const circle = document.getElementById(`circle${i}`);
    if (i <= step) circle.classList.add("active");
    else circle.classList.remove("active");
  }
}
function submitDiabetesForm() {
  const formData = new FormData(document.getElementById("DiabetesForm"));

  // Show loading
  document.getElementById("loadingIndicator").classList.remove("hidden");

  fetch("/predict-diabetes/", {
    method: "POST",
    body: formData,
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  })
  .then(res => res.json())
  .then(data => {
    setTimeout(() => {
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        document.getElementById("loadingIndicator").classList.add("hidden");
        alert(data.result || data.error);
      }
    }, 7000); // attendre 7 secondes
  })
  .catch(error => {
    setTimeout(() => {
      document.getElementById("loadingIndicator").classList.add("hidden");
      alert("Erreur : " + error);
    }, 7000);
  });
}

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : '';
}
