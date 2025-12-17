


document.addEventListener("DOMContentLoaded", function () {
    let index = 0;
    const slides = document.querySelectorAll(".slides img, .slides video");

    function showNextSlide() {
        slides[index].classList.remove("active");
        index = (index + 1) % slides.length; // Passe à l'image suivante en boucle
        slides[index].classList.add("active");
    }

    // Initialisation pour afficher la première image
    slides[index].classList.add("active");

    // Change l'image toutes les 3 secondes
    setInterval(showNextSlide, 3000);
    console.log("La premiere fonction!");

});


document.addEventListener("DOMContentLoaded", function () {
    const backToTopButton = document.getElementById("backToTop");

    if (!backToTopButton) {
        console.error("Le bouton 'Back to Top' n'existe pas !");
        return;
    }

    console.log("Le bouton a bien été trouvé !");

    // Ajoute un événement pour tester la fonctionnalité du bouton
    backToTopButton.addEventListener('click', function () {
        console.log("Le bouton a été cliqué !");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});




