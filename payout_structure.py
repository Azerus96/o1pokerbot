class PayoutStructure:
    def __init__(self, structure):
        self.structure = structure  # структура, например, "standard", "top-heavy", и т.д.
        # Можно добавить и другие структуры

    def calculate(self, num_players):
        # Логика расчета выплат на основе структуры и количества игроков
        if self.structure == 'standard':
            return max(0, num_players * 100 * 0.5)  # 50% пота
        elif self.structure == 'top-heavy':
            return max(0, num_players * 100 * 0.7) if num_players > 1 else 0
        return 0
