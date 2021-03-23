import random
import sys as system


def dessinPendu(nb):
    tab = [
        """
           +-------+
           |
           |
           |
           |
           |
        ==============
        """,
        """
           +-------+
           |       |
           |       O
           |
           |
           |
           |           
        ==============
        """,
        """
           +-------+
           |       |
           |       O
           |       |
           |
           |
           |
        ==============
        """,
        """
           +-------+
           |       |
           |       O
           |      -|
           |
           |
           |
        ==============
        """,
        """
           +-------+
           |       |
           |       O
           |      -|-
           |
           |
           |
        ==============
        """,
        """
           +-------+
           |       |
           |       O
           |      -|-
           |      |
           |
           |
        ==============
        """,
        """
           +-------+      F
           |       |       A
           |       O        T 
           |      -|-        A
           |      | |         L
           |                   I
           |                    T
        ==============           Y
        """
        ]
    return tab[nb]


def stat(text):
    dico = []
    for char in text:
        if char not in [" ", ",", ";", ":", "'", "\"", "(", ")", "!", "?"]:
            dico.append(char)
    return dico


def lines_as_str(lines, space=" "):
    text = ""
    for i in lines:
        text += i + space
    return text


def get_word_complexity(word):
    dico = []
    for i in word:
        if i not in dico:
            dico.append(i)
    return len(dico)/len(word)


class Game:

    def __init__(self, fileName, points=0, mots=None, gameNumber=1, wl=None, difficulty="normal"):
        self.fileName, self.gameNumber, self.mots, self.points, self.difficulty = fileName, gameNumber, mots, points, difficulty
        self.wl = wl if wl is not None else {"win": 0, "losses": 0}
        if mots is None:
            self.mots = []
            with open(fileName if fileName.endswith(".txt") else fileName + ".txt", "r") as f:
                for line in f:
                    self.mots.append(line.replace("\n", ""))
        self.over = False
        self.wrong, self.turn = 0, 1
        self.already_used = []
        self.word = self.mots[random.randint(0, len(self.mots))]
        self.letters = stat(self.word)
        self.nb_letters = len(self.word)
        self.lines = ['_' for i in range(self.nb_letters)]
        if difficulty == "easy":
            for n in range(self.nb_letters):
                if self.letters[n] == self.letters[0] or self.letters[n] == self.letters[-1]:
                    self.lines[n] = self.letters[n]
        print(">> Do '/help' for a list of commands")
        while not self.over:
            self.round()

    def round(self):
        print(f"Your points: {self.points}       Game number {self.gameNumber}       Difficulty: {self.difficulty}")
        if self.difficulty != "hard":
            print("Letters and words used: " + lines_as_str(self.already_used, ", "))
        print(dessinPendu(self.wrong))
        print(lines_as_str(self.lines) + "\n")
        user_input = input("Letter:").capitalize()
        if self.test_input(user_input):
            return
        if len(user_input) > 1:
            if user_input[0] == "/":
                self.command(user_input)
            elif user_input == self.word.capitalize():
                self._over("won")
            else:
                self.wrong += 1
                self.already_used.append(user_input)
        else:
            if user_input in self.letters and user_input not in self.already_used:
                for n in range(self.nb_letters):
                    if user_input == self.letters[n]:
                        self.lines[n] = self.letters[n]
            else:
                self.wrong += 1
            self.test_win()
            self.turn += 1
            if user_input not in self.already_used:
                self.already_used.append(user_input)

    def command(self, user_input):
        command = user_input[1:len(user_input)].capitalize()
        if command == "Help":
            print("""
            =============Help=================================================
            - word: prints the word to guess
            - stop, exit: exits the game
            - restart: starts a new game
            - rules: prints out the rules mate, kinda logic
            - stats, stat, info: prints the stats of the game (wis and losses)
            - difficulty {easy{e}, normal{n}, hard{h]}: sets the difficulty
            ==================================================================
                  """)
        elif command == "Word":
            print(f"Word: {self.word}\n")
        elif command == "Rules":
            print("""
                =========Rules=================================================
                - Basic hangman rules, you can guess the word just by typing it
                - Any letter typed that isn't new nor in the word counts as
                an error. Any wrong guess counts as an error.
                - At the end of a winning game you get points according to the
                size of the word and the number of turns taken to find it and
                the word complexity (ration of unique letters).
                ===============================================================
                  """)
        elif command in ["Stop", "Exit", "Quit"]:
            system.exit("User cancellation")
        elif command == "Restart":
            print("\n\n\n")
            Game(self.fileName)
        elif command in ["Stats", "Stat", "Info"]:
            print(f"\nNumber of Wins: {self.wl['win']}      Number of Losses: {self.wl['losses']}")
        else:
            command = command.split(" ")
            if command[0] == "Difficulty":
                if len(command[1]) > 1:
                    self.difficulty = command[1] if command[1] in ["easy", "normal", "hard"] else "easy"
                else:
                    if command[1] == "e":
                        self.difficulty = "easy"
                    if command[1] == "n":
                        self.difficulty = "normal"
                    elif command[1] == "h":
                        self.difficulty = "hard"
                    else:
                        print("Wrong input!")
                        return
                print(f"Difficulty set to: {self.difficulty} \n")
                if self.difficulty == "easy":
                    for n in range(self.nb_letters):
                        if self.letters[n] == self.letters[0] or self.letters[n] == self.letters[-1]:
                            self.lines[n] = self.letters[n]
            else:
                print(f"Unknown command '{command}'")
        input("Press 'Enter' to resume game...\n")

    def test_win(self):
        if self.test_full():
            self._over("won")
        elif self.wrong >= 6:
            self._over("lost")

    def test_full(self):
        return '_' not in self.lines

    def _over(self, state):
        self.over = True
        self.points += int(self.nb_letters + self.nb_letters * get_word_complexity(self.word) + self.nb_letters * len(self.word)/self.turn) if state == "won" else 0
        self.wl["win" if state == "won" else "losses"] += 1
        print(dessinPendu(self.wrong))
        print(f" The word was: {self.word}")
        print(f" You won in {self.turn} turns!") if state == "won" else print(f" You lost in {self.turn} turns...")
        play_again = input("\nDo you want to play again?  yes / no")
        if play_again == "yes":
            self.mots.remove(self.word)
            Game(self.fileName, self.points, self.mots, self.gameNumber + 1, self.wl, self.difficulty)
        else:
            system.exit('User cancelation')

    def test_input(self, user_input):
        try:
            if user_input[0] == " ":
                print("Wrong Input")
                return True
        except IndexError:
            print("Wrong Input")
            return True
        for char in user_input:
            if char in "-_éèôêï;.,?!§\\{([])}\"'#õã":
                print("Wrong Input")
                return True
        return False


if __name__ == '__main__':
    Game("lexique")
