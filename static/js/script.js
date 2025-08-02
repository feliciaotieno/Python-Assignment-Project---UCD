// --- Scroll to Top Button ---
const scrollBtn = document.getElementById('scrollToTop');
window.addEventListener('scroll', () => {
  if (window.scrollY > 150) {
    scrollBtn.style.display = 'block';
  } else {
    scrollBtn.style.display = 'none';
  }
});
scrollBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// --- Auto-focus Skip Link when tabbing ---
const skipLink = document.querySelector('.skip-link');
if (skipLink) {
  skipLink.addEventListener('focus', () => {
    skipLink.style.left = '16px';
    skipLink.style.top = '14px';
    skipLink.style.width = 'auto';
    skipLink.style.height = 'auto';
  });
  skipLink.addEventListener('blur', () => {
    skipLink.style.left = '-999px';
    skipLink.style.top = 'auto';
    skipLink.style.width = '1px';
    skipLink.style.height = '1px';
  });
}

// --- Flash message: Auto-scroll & fade-out ---
document.addEventListener('DOMContentLoaded', function() {
  // Flash messages
  const flash = document.querySelector('.flashes, .flash-success, .flash-error, .flash-info');
  if (flash) {
    flash.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => {
      flash.style.transition = 'opacity 0.7s';
      flash.style.opacity = '0';
      setTimeout(() => { flash.style.display = 'none'; }, 800);
    }, 4200);
  }

  // Toast notification
  const toast = document.getElementById('toast');
  if (toast && toast.textContent.trim()) {
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 3200);
  }
});

// --- Modal popup for Reflection Tips (reflection.html) ---
const openTips = document.getElementById('openTipsModal');
const closeTips = document.getElementById('closeTipsModal');
const tipsModal = document.getElementById('tipsModal');
if (openTips && closeTips && tipsModal) {
  openTips.addEventListener('click', () => {
    tipsModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  });
  closeTips.addEventListener('click', () => {
    tipsModal.style.display = 'none';
    document.body.style.overflow = '';
  });
  tipsModal.addEventListener('click', (e) => {
    if (e.target === tipsModal) {
      tipsModal.style.display = 'none';
      document.body.style.overflow = '';
    }
  });
}

// --- Fun Fact (Games page) ---
document.addEventListener('DOMContentLoaded', function () {
  // Fun facts array (customize these)
  const funFacts = [
    "Did you know? Playing logic games improves memory!",
    "Brain teasers boost your problem-solving skills.",
    "Studies show Sudoku can help reduce anxiety.",
    "People who play games regularly may process info faster.",
    "Logic puzzles train your brain to think creatively.",
    "Word games can expand your vocabulary and focus.",
    "The word 'palindrome' comes from Greek, meaning 'running back again.'",
    "The odds of winning the UK Lottery jackpot are about 1 in 45 million!",
    "Guessing numbers activates your brain’s logic and memory centers.",
    "Body Mass Index (BMI) was invented in the 1830s by a Belgian mathematician."
  ];
  let lastFactIndex = 0;

  // Fun fact button handler
  const showFactBtn = document.getElementById('show-fact-btn');
  const factText = document.getElementById('fun-fact-text');
  if (showFactBtn && factText) {
    showFactBtn.addEventListener('click', function () {
      let nextIndex;
      do {
        nextIndex = Math.floor(Math.random() * funFacts.length);
      } while (nextIndex === lastFactIndex && funFacts.length > 1);
      lastFactIndex = nextIndex;
      factText.textContent = funFacts[nextIndex];
      factText.classList.remove('highlight');
      void factText.offsetWidth; // trigger reflow for animation
      factText.classList.add('highlight');
    });
  }
});

// --- Table Sorting (for scoreboard) ---
document.addEventListener('DOMContentLoaded', function() {
  const tables = document.querySelectorAll('table');
  tables.forEach(function(table) {
    const headers = table.querySelectorAll('th');
    headers.forEach(function(th, colIdx) {
      th.addEventListener('click', function() {
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        const asc = th.classList.toggle('asc');
        headers.forEach(h => h !== th && h.classList.remove('asc', 'desc'));
        rows.sort((a, b) => {
          let ta = a.children[colIdx].textContent.trim();
          let tb = b.children[colIdx].textContent.trim();
          let cmp = (!isNaN(ta) && !isNaN(tb)) ? ta - tb : ta.localeCompare(tb);
          return asc ? cmp : -cmp;
        });
        rows.forEach(r => table.querySelector('tbody').appendChild(r));
      });
    });
  });
});

// --- Contact Form: Real-time Validation and Animation ---
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    let valid = true;
    const name = this.querySelector('[name="name"]');
    const email = this.querySelector('[name="email"]');
    const msg = this.querySelector('[name="message"]');

    // Simple validation
    [name, email, msg].forEach(field => field.classList.remove('invalid'));
    if (!name.value.trim()) {
      name.classList.add('invalid'); valid = false;
    }
    if (!email.value.match(/^.+@.+\..+$/)) {
      email.classList.add('invalid'); valid = false;
    }
    if (!msg.value.trim()) {
      msg.classList.add('invalid'); valid = false;
    }
    if (!valid) {
      e.preventDefault();
      showToast('Please fill in all fields with valid information.', 'error');
      return false;
    }
  });
}

// --- Toast notification helper ---
function showToast(message, type = "success") {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.style.background = (type === "error") ? "#f44336" : "#4caf50";
  toast.style.color = "#fff";
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 3500);
}

