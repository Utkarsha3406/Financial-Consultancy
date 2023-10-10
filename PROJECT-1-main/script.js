// Dashboard Page JavaScript

// Get the card containers
const cards = document.querySelectorAll('.dashboard-card');

// Add a click event listener to each card
cards.forEach(function (card) {
    card.addEventListener('click', () => {
      // Get the card title
      const title = card.querySelector('h2').textContent;

      // Show an alert with the card title
      alert(`You clicked on the "${title}" card!`);
    });
  });
