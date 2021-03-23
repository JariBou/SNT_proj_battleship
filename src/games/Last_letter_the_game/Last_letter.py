from random import randint


class Last_letter:

    def __init__(self):
        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                         "u", "v", "w", "x", "y", "z"]
        self.voyelles = ["a", "e", "i", "o", "u"]
        self.cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                     "v", "w", "x", "y", "z"]

        t = 1
        preum = self.alphabet[randint(0, 26)]
        print("First letter: ", preum)
        self.mots = []
        der = []
        self.dernier = None
        self.points = 0
        turn = 1

        while t == 1:
            self.input = input("")
            pr = self.input[0]

            if self.input == "stop":
                exit()

            if self.dernier is None:
                self.dernier = preum

            if self.test_word(self.input):
                if len(self.input) == 1:
                    print("Wrong, only one letter....")
                    print("Game over!! Not enough letters!")
                    print("Number of turns: ", turn, "    Points: ", self.points)
                    lon = len(self.input)
                    for i in range(lon):
                        if self.input[i] == "y":
                            self.points -= 10
                        if self.input[i] in self.voyelles:
                            self.points -= 3
                        if self.input[i] in self.cons:
                            self.points -= 1
                    turn = 1
                    self.end()

                elif len(self.input) >= 2:
                    if self.input in self.mots:
                        print("Game over!! Word already used!")
                        print("Number of turns: ", turn, "    Points: ", self.points)
                        self.points = 0
                        lon = len(self.input)
                        for i in range(lon):
                            if self.input[i] == "y":
                                self.points -= 10
                            elif self.input[i] in self.voyelles:
                                self.points -= 3
                            elif self.input[i] in self.cons:
                                self.points -= 1
                        turn = 1
                        self.end()
                    elif self.dernier != pr:
                        print("Game over!! Wrong first letter!")
                        print("Number of turns: ", turn, "    Points: ", self.points)
                        self.points = 0
                        lon = len(self.input)
                        for i in range(lon):
                            if self.input[i] == "y":
                                points -= 10
                            elif self.input[i] in self.voyelles:
                                points -= 3
                            elif self.input[i] in self.cons:
                                points -= 1
                        turn = 1
                        self.end()
                    else:
                        lon = len(self.input)
                        for i in range(lon):
                            if self.input[i] == "y":
                                points += 10
                            elif self.input[i] in self.voyelles:
                                points += 3
                            elif self.input[i] in self.cons:
                                points += 1
                        self.mots.append(str(self.input))
                        turn += 1
                        self.dernier = self.input[-1]
                        print(self.input, " -----", self.dernier, "                                                         Points: ",
                              points)

    def end(self):
        self.mots.clear()
        print("")
        print("")
        print("Do you want to play again?")
        print("1: Yes")
        b = int(input("2: No"))
        if b == 1:
            Last_letter()
        if b == 2:
            exit()
        else:
            self.end()

    def test_word(self, w):
        lon = len(w)
        for i in range(0, lon):
            if w[i] in self.alphabet:
                i += 1
            else:
                print("Nope, You cannot use special characters")
                return False
        return True


if __name__ == '__main__':
    Last_letter()
