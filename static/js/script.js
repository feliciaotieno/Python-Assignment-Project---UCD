// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('a[href^="#"]');
  for (let link of links) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // Suggest-a-Game form logic
  const suggestForm = document.getElementById('suggest-form');
  if (suggestForm) {
    suggestForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const val = this.suggestion.value.trim();
      const feedback = document.getElementById('suggest-feedback');
      if (val.length < 3) {
        feedback.textContent = "Please enter a more detailed suggestion.";
        feedback.style.display = 'block';
        feedback.style.color = 'crimson';
        this.suggestion.classList.add('invalid');
        this.suggestion.focus();
        return;
      }
      this.suggestion.classList.remove('invalid');
      feedback.textContent = "";
      showToast('Thanks for your suggestion: "' + val + '"!');
      this.reset();
    });
  }

  // Fun Facts toggle logic
  const factsToggle = document.getElementById('facts-toggle');
  const factsList = document.getElementById('facts-list');
  const arrow = document.getElementById('arrow');
  if (factsToggle && factsList && arrow) {
    factsToggle.addEventListener('click', function() {
      if (factsList.style.display === 'none' || factsList.style.display === '') {
        factsList.style.display = 'block';
        arrow.textContent = '▲';
      } else {
        factsList.style.display = 'none';
        arrow.textContent = '▼';
      }
    });
  }

  // Scoreboard sorting logic (if you have one)
  const scoreboard = document.getElementById('scoreboard');
  if (scoreboard) {
    scoreboard.querySelectorAll('th').forEach((header, idx) => {
      header.style.cursor = 'pointer';
      header.title = 'Sort by this column';
      header.addEventListener('click', function() {
        const rows = Array.from(scoreboard.tBodies[0].rows);
        const isNumber = idx > 0;
        rows.sort((a, b) => {
          let v1 = a.cells[idx].textContent, v2 = b.cells[idx].textContent;
          if (isNumber) { v1 = parseFloat(v1)||0; v2 = parseFloat(v2)||0; }
          return v2 - v1;
        });
        rows.forEach(r => scoreboard.tBodies[0].appendChild(r));
      });
    });
  }
});

// Scroll-to-top button logic
const scrollBtn = document.getElementById('scrollToTop');
if (scrollBtn) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 250) scrollBtn.style.display = 'block';
    else scrollBtn.style.display = 'none';
  });
  scrollBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// Toast notification function
function showToast(msg, color="#4caf50") {
  const toast = document.getElementById('toast');
  if (toast) {
    toast.textContent = msg;
    toast.style.background = color;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 2800);
  }
}

// Keyboard shortcuts (accessibility)
document.addEventListener('keydown', function(e) {
  if (e.altKey && !e.shiftKey) {
    if (e.key.toLowerCase() === 'g') window.location.href = '/games';
    if (e.key.toLowerCase() === 'r') window.location.href = '/reflect';
    if (e.key.toLowerCase() === 's') window.location.href = '/stats';
  }
});

// Debug: console message for stats page
if (window.location.href.includes('stats')) {
  console.log("Welcome to your stats dashboard!");
}
// Reflection Tips Modal
document.addEventListener('DOMContentLoaded', function() {
  const openModal = document.getElementById('openTipsModal');
  const closeModal = document.getElementById('closeTipsModal');
  const modal = document.getElementById('tipsModal');
  if (openModal && closeModal && modal) {
    openModal.onclick = () => { modal.style.display = 'flex'; };
    closeModal.onclick = () => { modal.style.display = 'none'; };
    window.onclick = (e) => { if (e.target === modal) modal.style.display = 'none'; };
  }
});
