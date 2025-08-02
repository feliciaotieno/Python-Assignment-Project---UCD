"""
================================
    MindForge Web Application
================================

Built using Flask as part of a Python assignment.
Features:
- Game hub with interactive games
- Reflection journal with persistent storage
- Statistics and mood analysis
- Clean code structure and full route handling
"""

from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this before production


# JSON file for saving reflections #
REFLECTION_FILE = "reflections.json"

# Load reflections from file or initialize empty list #
if os.path.exists(REFLECTION_FILE):
    with open(REFLECTION_FILE, "r") as f:
        reflections = json.load(f)
else:
    reflections = []

# In-memory tracking for game stats (not saved to file yet)
game_stats = {
    "guess_attempts": 0,
    "guess_wins": 0,
    "lottery_plays": 0,
    "lottery_matches": 0,
    "palindrome_checks": 0,
    "palindrome_hits": 0,
    "sudoku_plays": 0
}

# Home page #
@app.route('/')
def home():
    total_reflections = len(reflections)
    common_mood = Counter(entry['mood'] for entry in reflections).most_common(1)
    common_mood = common_mood[0][0] if common_mood else "None yet"
    quotes = [
        "Every accomplishment starts with the decision to try.",
        "The mind is not a vessel to be filled but a fire to be kindled.",
        "Learning never exhausts the mind.",
        "Small daily improvements are the key to staggering long-term results.",
        "The greatest discovery of all time is that a person can change their future by merely changing their attitude.",
        "You are braver than you believe, stronger than you seem, and smarter than you think."
    ]
    import random
    quote = random.choice(quotes)
    latest_reflection = reflections[-1] if reflections else None
    total_games_played = (
        game_stats["guess_attempts"] + 
        game_stats["lottery_plays"] + 
        game_stats["palindrome_checks"]
        # add more if you implement more games!
    )

    return render_template(
        'index.html',
        total_reflections=total_reflections,
        common_mood=common_mood,
        quote=quote,
        latest_reflection=latest_reflection,
        total_games_played=total_games_played,
        game_stats=game_stats
    )

# Games index #
@app.route('/games')
def games():
    return render_template('games.html', game_stats=game_stats)

# Guess the number game
@app.route('/games/guess', methods=['GET', 'POST'])
def guess_number():
    import random
    message = ""
    secret = 7  # or randomize if you want
    redirect_delay = None  # seconds

    if request.method == 'POST':
        game_stats["guess_attempts"] += 1
        try:
            guess = int(request.form.get('guess'))
            if guess < secret:
                message = "Too low!"
            elif guess > secret:
                message = "Too high!"
            else:
                message = "🎉 Correct! You guessed it!"
                game_stats["guess_wins"] += 1
            redirect_delay = 5  # seconds to show result before redirecting
        except Exception:
            message = "Please enter a valid number."
            redirect_delay = 5

    return render_template('guess_number.html', message=message, redirect_delay=redirect_delay)

# Lottery draw and match results
@app.route('/games/lottery', methods=['GET', 'POST'])
def lottery():
    import random
    result = ""
    redirect_delay = None
    user_numbers = []
    drawn_numbers = random.sample(range(1, 50), 6)

    if request.method == 'POST':
        game_stats["lottery_plays"] += 1
        try:
            for i in range(6):
                num = int(request.form.get(f'num{i+1}'))
                if num < 1 or num > 49:
                    raise ValueError("Each number must be between 1 and 49.")
                user_numbers.append(num)
            matches = set(user_numbers) & set(drawn_numbers)
            game_stats["lottery_matches"] += len(matches)
            result = f"🎉 You matched {len(matches)} numbers!<br>Winning numbers: {drawn_numbers}<br>Your numbers: {user_numbers}<br>Matched: {sorted(matches)}"
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"
        redirect_delay = 5

    return render_template('lottery.html', result=result, redirect_delay=redirect_delay)

# Palindrome check
@app.route('/games/palindrome', methods=['GET', 'POST'])
def palindrome():
    result = ""
    redirect_delay = None

    if request.method == 'POST':
        game_stats["palindrome_checks"] += 1
        word = request.form.get('word', '').strip()
        if word == "":
            result = "⚠️ Please enter a word."
        elif word.lower() == word[::-1].lower():
            result = f"✅ '{word}' is a palindrome!"
            game_stats["palindrome_hits"] += 1
        else:
            result = f"❌ '{word}' is not a palindrome."
        redirect_delay = 5

    return render_template('palindrome.html', result=result, redirect_delay=redirect_delay)

# Helper function to calculate BMI and return category
def calculate_bmi(weight, height):
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be greater than zero.")
    
    bmi_value = weight / (height ** 2)
    bmi_value = round(bmi_value, 2)

    if bmi_value < 18.5:
        category = "Underweight"
    elif bmi_value < 25:
        category = "Normal weight"
    elif bmi_value < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi_value, category

@app.route('/games/bmi', methods=['GET', 'POST'])
def bmi():
    result = ""
    redirect_delay = None

    if request.method == 'POST':
        try:
            weight = float(request.form.get('weight', '').strip())
            height = float(request.form.get('height', '').strip())
            bmi_value, category = calculate_bmi(weight, height)
            result = f"Your BMI is {bmi_value} ({category})"
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"
        redirect_delay = 5

    return render_template('bmi.html', result=result, redirect_delay=redirect_delay)

# Sudoku game
@app.route('/games/sudoku', methods=['GET', 'POST'])
def sudoku():
    result = ""
    redirect_delay = None
    board = []

    if request.method == 'POST':
        game_stats["sudoku_plays"] += 1
        try:
            for i in range(9):
                row = request.form.get(f'row{i}', '').strip()
                row_vals = list(map(int, row.split()))
                if len(row_vals) != 9:
                    raise ValueError("Each row must have exactly 9 integers.")
                if any(v < 1 or v > 9 for v in row_vals):
                    raise ValueError("Sudoku numbers must be between 1 and 9.")
                board.append(row_vals)
            if is_valid_sudoku(board):
                result = "✅ This is a valid Sudoku solution!"
            else:
                result = "❌ This is NOT a valid Sudoku solution."
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"
        redirect_delay = 5

    return render_template('sudoku.html', result=result, redirect_delay=redirect_delay)

def is_valid_sudoku(grid):
    def is_valid_group(group):
        return sorted(group) == list(range(1, 10))

    # Check rows
    for row in grid:
        if not is_valid_group(row):
            return False

    # Check columns
    for col in range(9):
        if not is_valid_group([grid[row][col] for row in range(9)]):
            return False

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(grid[box_row + i][box_col + j])
            if not is_valid_group(block):
                return False

    return True

@app.route('/set-name', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            session['name'] = name
            return redirect(url_for('home'))
    return render_template('set_name.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('home'))

from flask import render_template, request, redirect, url_for, session, flash
from collections import Counter
import datetime
import json
import os

def load_reflections():
    if os.path.exists("reflections.json"):
        with open("reflections.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_reflections(reflections):
    with open("reflections.json", "w", encoding="utf-8") as f:
        json.dump(reflections, f, indent=2, ensure_ascii=False)

@app.route('/reflect', methods=['GET', 'POST'])
def reflect():
    reflections = load_reflections()
    error = None

    # POST: Add a new reflection
    if request.method == "POST":
        mood = request.form.get("mood")
        tag = request.form.get("tag")
        notes = request.form.get("notes")
        if not mood or not notes:
            error = "Mood and Reflection are required."
        else:
            new_entry = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "mood": mood,
                "tag": tag or "general",
                "notes": notes.strip()
            }
            reflections.append(new_entry)
            save_reflections(reflections)
            flash("Reflection submitted!", "success")
            return redirect(url_for('reflect'))

    # Calculate mood_counts
    mood_counts = Counter(entry['mood'] for entry in reflections) if reflections else {}

    # Latest reflection
    latest_reflection = reflections[-1] if reflections else None

    # Streak calculation 
    streak = 1
    if len(reflections) > 1:
        streak = 1
        for i in range(1, len(reflections)):
            if reflections[-i]['timestamp'][:10] == reflections[-i-1]['timestamp'][:10]:
                streak += 1
            else:
                break

    return render_template(
        'reflection.html',
        mood_counts=mood_counts,
        reflections=reflections,
        latest_reflection=latest_reflection,
        streak=streak,
        error=error
    )

# Stats page - mood counts, recent entry, chart
@app.route('/stats')
def stats():
    total = len(reflections)
    mood_counts = Counter(entry['mood'] for entry in reflections)
    tag_counts = Counter(entry.get('tag', 'general') for entry in reflections)
    latest = reflections[-1] if reflections else None

    selected_mood = request.args.get('mood')
    selected_tag = request.args.get('tag')
    keyword = request.args.get('search', '').lower()

    filtered = reflections
    if selected_mood:
        filtered = [r for r in filtered if r['mood'].lower() == selected_mood.lower()]
    if selected_tag:
        filtered = [r for r in filtered if r.get('tag', 'general').lower() == selected_tag.lower()]
    if keyword:
        filtered = [r for r in filtered if keyword in r['notes'].lower()]

    # Mood trend chart data
    from collections import defaultdict
    mood_trend = {"days": [], "data": {}}
    if reflections:
        day_mood = defaultdict(lambda: defaultdict(int))
        for entry in reflections:
            day = entry['timestamp'][:10]
            day_mood[day][entry['mood']] += 1
        sorted_days = sorted(day_mood.keys())
        all_moods = sorted({m for v in day_mood.values() for m in v})
        mood_trend = {
            "days": sorted_days,
            "data": {mood: [day_mood[day].get(mood, 0) for day in sorted_days] for mood in all_moods}
        }

    return render_template(
        'stats.html',
        reflections=filtered,
        total=len(reflections),
        mood_counts=mood_counts,
        tag_counts=tag_counts,
        latest=latest,
        game_stats=game_stats,
        mood_trend=mood_trend,
    )

# Export reflections.json for download
@app.route('/export')
def export_reflections():
    from flask import make_response
    response = make_response(json.dumps(reflections, indent=2))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=reflections.json'
    return response

# Contact page

CONTACTS_FILE = "contacts.json"

def save_contact(data):
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            contacts = json.load(f)
    else:
        contacts = []
    contacts.append(data)
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not email or not message:
            flash("All fields are required.", "danger")
        else:
            save_contact({
                "name": name,
                "email": email,
                "message": message
            })
            flash("Thank you for contacting us! We'll get back to you soon.", "success")
            return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

