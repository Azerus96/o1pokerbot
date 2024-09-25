from mccfr import MCCFR

class PokerPlayer:
    def __init__(self, name, stack, use_mccfr=True, iterations=1000):
        self.name = name
        self.stack = stack
        self.initial_stack = stack
        self.history = []
        self.dossier = {}
        self.use_mccfr = use_mccfr

        self.strategy_system = MCCFR(iterations) if use_mccfr else BasicPokerStrategy()

    # Добавьте остальные методы, необходимые для вашего игрока
