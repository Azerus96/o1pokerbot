class TournamentHistory:
    def __init__(self):
        self.games = []  # Хранилище историй игр

    def add_game(self, winner, players):
        game_data = {
            "winner": winner.name,
            "stack": winner.stack,
            "players": {player.name: player.stack for player in players}
        }
        self.games.append(game_data)

    def get_all_games(self):
        return self.games
