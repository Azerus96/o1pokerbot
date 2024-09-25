import os
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from config import PokerTournamentConfig
from player import PokerPlayer
from poker_game import PokerGame, setup_tournament
from logging_system import Logger
from tournament_history import TournamentHistory

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

logger = Logger()
history = TournamentHistory()
tournament = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournament')
def tournament_page():
    return render_template('tournament.html')

@app.route('/history')
def history_page():
    games_data = history.get_all_games()
    return render_template('history.html', games=games_data)

@app.route('/register', methods=['POST', 'GET'])
def register():
    global tournament
    if request.method == 'POST':
        player_name = request.form['player_name']
        player_stack = int(request.form['player_stack'])
        new_player = PokerPlayer(name=player_name, stack=player_stack)
        tournament.players.append(new_player)
        logger.log_event(f"Player {player_name} зарегистрирован.")
        return redirect('/tournament')

    return render_template('player.html')

@app.route('/start_tournament', methods=['POST'])
def start_tournament():
    max_players = int(request.form['max_players'])
    bot_players = int(request.form['bot_players'])
    initial_stack = int(request.form['initial_stack'])
    round_duration = int(request.form['round_duration'])
    payout_structure = request.form['payout_structure']  # Новая переменная для условия выплат
    allow_late_registration = 'allow_late_registration' in request.form
    late_registration_rounds = int(request.form['late_registration_rounds'])

    global tournament
    tournament = setup_tournament(max_players, bot_players, initial_stack, 
                                   round_duration, payout_structure, 
                                   allow_late_registration, late_registration_rounds)
    return redirect('/tournament')

if __name__ == "__main__":
    socketio.run(app, debug=True)
