class Game:

    def __init__(self):
        self.p = Player(20)
        print(f"Player Health:{self.p.health}                      Ennemi Health: N/A")


class Player:

    def __init__(self, health):
        self.health = health


if __name__ == '__main__':
    Game()