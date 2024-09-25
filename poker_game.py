from collections import Counter
from config import PokerTournamentConfig
from payout_structure import PayoutStructure

class PokerGame:
    def __init__(self, players, config):
        self.players = players
        self.config = config
        self.current_round = 0
        self.history = []

    def can_register(self):
        if not self.config.allow_late_registration:
            return False
        return self.current_round <= self.config.late_registration_rounds

    async def play_round(self):
        # Логика по проведению раунда
        pass
    
    def distribute_payouts(self, winner):
        payout_structure = PayoutStructure(self.config.payout_structure)
        payout = payout_structure.calculate(len(self.players))
        winner.stack += payout

def setup_tournament(max_players=160, bot_players=10, initial_stack=10000,
                     round_duration=6, payout_structure='standard',
                     allow_late_registration=True, late_registration_rounds=2):
    config = PokerTournamentConfig()
    config.allow_late_registration = allow_late_registration
    config.late_registration_rounds = late_registration_rounds
    config.starting_stack = initial_stack
    config.payout_structure = payout_structure

    players = []
    for i in range(bot_players):
        bot = PokerPlayer(name=f'Bot {i + 1}', stack=initial_stack)
        players.append(bot)
    
    return PokerGame(players, config)
