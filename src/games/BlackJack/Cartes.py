import copy


class Carte:

    def __init__(self, color: str, name: str, aceValue: int):
        self.color = color
        self.name = name
        self.aceValue = aceValue
        self.value = 0
        self.calculateValue()

    def calculateValue(self):
        if self.name in ["roi", "valet", "dame"]:
            self.value = 10
        elif self.name == "as":
            self.value = self.aceValue
        else:
            self.value = int(self.name)

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def getCardTextureName(self):
        return f"{self.name}_{self.color}.gif"

    def get_id(self):
        return f"{self.name}_{self.color}"

    def setValue(self, val: int):
        self.value = val

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Carte):
            return self.get_id() == other.get_id()
        elif isinstance(other, int):
            return self.get_value() == other

    def __str__(self):
        return f"{self.name} de {self.color} ({self.value})"


class PaquetDeCartes:

    def __init__(self, aceValue: int):
        self.card_colors = ["coeur", "pique", "carreau", "trefle"]
        self.aceValue = aceValue
        self.heads = ["roi", "valet", "dame"]
        self.cardsList = list(range(2, 11)) + self.heads + ["as"]
        self.cards = []
        self.create()

    def create(self):
        for color in self.card_colors:
            for name in self.cardsList:
                self.cards.append(Carte(color, str(name), self.aceValue))
        return self

    def __str__(self):
        concat = ""
        for k in range(4):
            for i in range(14):
                concat += f"{str(self.cards[i + k * 14])} - "
            concat += "\n"
        return concat

    def getCards(self):
        return self.cards


class Pile:

    def __init__(self, li: list):
        self.pile = copy.deepcopy(li)

    def pick(self):
        return self.pile.pop()

    def lenght(self):
        return len(self.pile)

    def get(self):
        return self.pile

    def set(self, li: list):
        self.pile = copy.deepcopy(li)


if __name__ == '__main__':
    p = PaquetDeCartes(11).create()
    print(p)

