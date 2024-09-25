from collections import Counter
from config import PokerTournamentConfig
from payout_structure import PayoutStructure
from player import PokerPlayer

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
        payout = self.config.payout_structure.calculate(len(self.players))
        winner.stack += payout

    def get_table_state(self):
        # Реализуйте эту функцию для возврата текущего состояния стола
        pass

def setup_tournament(max_players=160, bot_players=10, initial_stack=10000,
                     round_duration=6, payout_structure='standard',
                     allow_late_registration=True, late_registration_rounds=2,
                     mccfr_strategy=None):
    config = PokerTournamentConfig()
    config.round_duration_minutes = round_duration
    config.starting_stack = initial_stack
    config.payout_structure = PayoutStructure(payout_structure)
    config.allow_late_registration = allow_late_registration
    config.late_registration_rounds = late_registration_rounds

    players = []
    for i in range(min(bot_players, max_players)):
        bot = PokerPlayer(name=f'Bot {i + 1}', stack=initial_stack, strategy=mccfr_strategy)
        players.append(bot)
    
    return PokerGame(players, config)
