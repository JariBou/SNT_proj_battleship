from src.games.BlackJack.Cartes import Carte


class Joueur:

    def __init__(self, name: str, type: str):
        self.name = name
        self.hand = []
        self.type = type

    def draw(self, card: Carte):
        self.hand.append(card)

    def reset(self):
        self.hand = []

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_points(self):
        return sum([card.get_value() for card in self.hand]) if self.hand else 0

    def __str__(self):
        return f"{self.name} ; hand: {[str(card) for card in self.hand]}({self.get_points()})"
