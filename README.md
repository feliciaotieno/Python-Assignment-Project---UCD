# MindForge

MindForge is a Flask-based web application designed for logic games, mood reflection, and personal statistics. This project demonstrates strong skills in Python, Flask, modern HTML5, CSS3, and JavaScript, as well as user-centric, accessible web design.

---

## Project Overview

MindForge provides users with a collection of classic logic games and a private reflection journal. Users can track moods, see their game and reflection statistics, and enjoy a responsive, visually cohesive UI. All data is stored locally for privacy.

---

repo:
  github_url: https://github.com/feliciaotieno/Python-Assignment-Project---UCD.git
  render_url: https://python-assignment-project-ucd.onrender.com

## Features

- **Games:**  
  - Guess the Number  
  - Palindrome Checker  
  - Lottery Game  
  - Sudoku Checker  
  - BMI Calculator

- **Reflections:**  
  - Mood and tag tracking  
  - Progress streaks  
  - Reflection log (private and persistent)

- **Statistics:**  
  - Game stats, high scores, and a reflection log  
  - Visualizations with Chart.js

- **User Interface:**  
  - Responsive layout and sticky sidebars  
  - Modals for reflection tips  
  - Modern, consistent color theme  
  - Accessible forms and navigation

- **JavaScript Interactivity:**  
  - Scroll-to-top button  
  - Modal popups  
  - Real-time form validation  
  - Table sorting  

---

## Technology Stack

- **Backend:** Python 3, Flask  
- **Frontend:** HTML5, CSS3, JavaScript (ES6), Chart.js  
- **Deployment:** Compatible with Render.com

---

## How to Run Locally

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/mindforge.git
    cd mindforge
    ```

2. **Set up the virtual environment and install requirements:**
    ```sh
    python -m venv venv
    source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```sh
    flask run
    ```
    Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Deployment Notes

- Deployable on [Render.com](https://render.com/) with Python environment and Gunicorn.  
- All dependencies are listed in `requirements.txt` and set `web: gunicorn app:app` in `Procfile` needed.
- Data files (`reflections.json`, `game_stats.json`) are stored locally for the demo.

---

## Accessibility & Best Practices

- "Skip to main content" link for screen readers and keyboard navigation
- Sufficient color contrast
- Fully responsive layout
- All forms are validated on both client and server sides
- Descriptive alt text on all images

---

## References & Image Credits

- **Logo and background images:**  
  - Sourced from [Unsplash](https://unsplash.com/) (free for commercial and personal use).
- **Frontend Libraries:**  
  - [Chart.js](https://www.chartjs.org/) for charts and data visualization.

---

## Author

Developed by Felicia Otieno, 2025.  
This project is for educational and demonstration purposes.

---

