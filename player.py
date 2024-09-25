from mccfr import MCCFR
import pickle
import random

class PokerPlayer:
    def __init__(self, name, stack, strategy=None):
        self.name = name
        self.stack = stack
        self.initial_stack = stack
        self.history = []
        self.dossier = {}
        self.strategy = strategy if strategy else BasicPokerStrategy()

    def make_decision(self, game_state):
        decision = self.strategy.decide(game_state)
        self.store_decision(game_state, decision)
        return decision

    def store_decision(self, game_state, decision):
        self.history.append({
            "game_state": game_state,
            "decision": decision
        })

    def record_opponent_action(self, opponent_name, action):
        if opponent_name not in self.dossier:
            self.dossier[opponent_name] = {"aggro": 0, "fold": 0, "call": 0, "bluff": 0}
        self.dossier[opponent_name][action] += 1

    def adjust_strategy(self):
        if isinstance(self.strategy, MCCFR):
            self.strategy.run_iterations(self.history)

    def save_state(self, file_name=None):
        if file_name is None:
            file_name = f'{self.name}_state.pkl'
        with open(file_name, 'wb') as file:
            pickle.dump({
                "history": self.history,
                "dossier": self.dossier,
                "strategy": self.strategy.strategy if isinstance(self.strategy, MCCFR) else None
            }, file)

    def load_state(self, file_name):
        with open(file_name, 'rb') as file:
            state = pickle.load(file)
            self.history = state["history"]
            self.dossier = state["dossier"]
            if isinstance(self.strategy, MCCFR) and state["strategy"]:
                self.strategy.strategy = state["strategy"]

class BasicPokerStrategy:
    def decide(self, game_state):
        return random.choice(['fold', 'call', 'raise'])
