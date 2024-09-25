class PayoutStructure:
    def __init__(self, structure):
        if isinstance(structure, str):
            self.structure = structure
        elif isinstance(structure, dict):
            self.structure = structure
        else:
            raise ValueError("Invalid payout structure")

    def calculate(self, num_players):
        if isinstance(self.structure, str):
            if self.structure == 'standard':
                return self._calculate_standard(num_players)
            elif self.structure == 'top-heavy':
                return self._calculate_top_heavy(num_players)
            else:
                raise ValueError(f"Unknown payout structure: {self.structure}")
        elif isinstance(self.structure, dict):
            return self._calculate_custom(num_players)
        else:
            raise ValueError("Invalid payout structure")

    def _calculate_standard(self, num_players):
        total_prize = num_players * 100  # Предполагаем, что каждый игрок вносит 100
        return {
            1: total_prize * 0.5,
            2: total_prize * 0.3,
            3: total_prize * 0.2
        }

    def _calculate_top_heavy(self, num_players):
        total_prize = num_players * 100
        return {
            1: total_prize * 0.7,
            2: total_prize * 0.2,
            3: total_prize * 0.1
        }

    def _calculate_custom(self, num_players):
        total_prize = num_players * 100
        return {pos: total_prize * percentage for pos, percentage in self.structure.items()}
