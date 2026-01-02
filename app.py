from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'a_much_more_secret_key'

DIFFICULTY_LEVELS = {
    'easy': {'range': (1, 50), 'attempts': 10},
    'medium': {'range': (1, 100), 'attempts': 7},
    'hard': {'range': (1, 200), 'attempts': 5}
}
LEADERBOARD_FILE = 'leaderboard.json'

def get_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            # Check if file is empty
            if os.fstat(f.fileno()).st_size == 0:
                return []
            return json.load(f)
    except (json.JSONDecodeError):
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=4)

@app.route('/')
def index():
    if 'number' in session:
        return render_template('index.html', game_in_progress=True, history=session.get('history', []), attempts_left=session.get('attempts_left'))
    return render_template('index.html', game_in_progress=False, difficulties=DIFFICULTY_LEVELS.keys())

@app.route('/start', methods=['POST'])
def start_game():
    difficulty = request.form.get('difficulty', 'medium')
    if difficulty not in DIFFICULTY_LEVELS:
        flash('Invalid difficulty selected. Defaulting to medium.', 'error')
        difficulty = 'medium'

    level = DIFFICULTY_LEVELS[difficulty]
    session['difficulty'] = difficulty
    session['number'] = random.randint(*level['range'])
    session['attempts_left'] = level['attempts']
    session['history'] = []
    
    flash(f'New {difficulty.capitalize()} game started! Guess a number between {level["range"][0]} and {level["range"][1]}.', 'info')
    return redirect(url_for('index'))

@app.route('/guess', methods=['POST'])
def guess():
    if 'number' not in session:
        flash('A new game has not been started. Please select a difficulty.', 'info')
        return redirect(url_for('index'))

    try:
        user_guess = int(request.form['guess'])
    except (ValueError, TypeError):
        flash('Please enter a valid number.', 'error')
        return redirect(url_for('index'))

    session['attempts_left'] -= 1
    session['history'].append(user_guess)
    session.modified = True

    if user_guess < session['number']:
        flash('Too low! Try again.', 'warning')
    elif user_guess > session['number']:
        flash('Too high! Try again.', 'warning')
    else:
        attempts_taken = DIFFICULTY_LEVELS[session['difficulty']]['attempts'] - session['attempts_left']
        flash(f'Correct! The number was {session["number"]}. It took you {attempts_taken} attempts.', 'success')
        
        leaderboard = get_leaderboard()
        leaderboard.append({'difficulty': session['difficulty'], 'attempts': attempts_taken})
        leaderboard.sort(key=lambda x: x['attempts'])
        save_leaderboard(leaderboard[:10]) # Keep top 10

        session.pop('number', None)
        return redirect(url_for('leaderboard'))

    if session['attempts_left'] <= 0:
        flash(f'Game Over! The number was {session["number"]}.', 'error')
        session.pop('number', None)
        return redirect(url_for('index'))
    
    if len(session['history']) >= 3:
        if session['number'] % 2 == 0:
            flash('Hint: The number is even.', 'info')
        else:
            flash('Hint: The number is odd.', 'info')

    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', leaderboard=get_leaderboard())

@app.route('/reset')
def reset():
    session.clear()
    flash('Game reset. Please select a difficulty to start a new game.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)