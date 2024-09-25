from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from player import PokerPlayer
from poker_game import setup_tournament
from mccfr import MCCFR
from logging_system import Logger
import os

app = Flask(__name__)
socketio = SocketIO(app)

tournament = None
logger = Logger()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournament')
def tournament_page():
    return render_template('tournament.html')

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
    global tournament
    max_players = int(request.form['max_players'])
    bot_players = int(request.form['bot_players'])
    initial_stack = int(request.form['initial_stack'])
    round_duration = int(request.form['round_duration'])
    payout_structure = request.form['payouts']
    allow_late_registration = 'allow_late_registration' in request.form
    late_registration_rounds = int(request.form['late_registration_rounds'])

    tournament = setup_tournament(
        max_players=max_players,
        bot_players=bot_players,
        initial_stack=initial_stack,
        round_duration=round_duration,
        payout_structure=payout_structure,
        allow_late_registration=allow_late_registration,
        late_registration_rounds=late_registration_rounds,
        mccfr_strategy=mccfr_strategy
    )
    logger.log_event("Турнир начат с заданными параметрами.")
    return redirect('/tournament')

def update_tournament_state(state):
    socketio.emit('update_tournament', state)

@socketio.on('player_action')
def handle_player_action(data):
    global tournament
    player_name = data['player_name']
    action = data['action']
    raise_value = data.get('raise', 0)

    for player in tournament.players:
        if player.name == player_name:
            if action == 'fold':
                logger.log_event(f"Player {player_name} folded.")
            elif action == 'call':
                logger.log_event(f"Player {player_name} called.")
            elif action == 'raise':
                logger.log_event(f"Player {player_name} raised by {raise_value}.")
            break

    update_tournament_state(tournament.get_table_state())

def start_flask():
    socketio.run(app, host='0.0.0.0', port=10000)

if __name__ == "__main__":
    mccfr_strategy = MCCFR()
    if os.path.exists('mccfr_strategy.pkl'):
        mccfr_strategy.load_strategy('mccfr_strategy.pkl')

    tournament = setup_tournament(
        max_players=160,
        bot_players=10,
        initial_stack=10000,
        round_duration=6,
        payout_structure='standard',
        allow_late_registration=True,
        late_registration_rounds=2,
        mccfr_strategy=mccfr_strategy
    )

    start_flask()
