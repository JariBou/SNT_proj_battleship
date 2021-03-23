from random import randint
from csv import *

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
voyelles = ["a", "e", "i", "o", "u"]
cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
            "v", "w", "x", "y", "z"]

## y = 10 points
## voyelles = 3 points
## consonnes = 2 point

print("Rules: You have to write a word that starts with the las letter of the previous word.")
print("The game reminds you of the last written word and the last letter.")
print("The game gives you the letter for the first word.")
print("You can close the game at any moment by typing 'stop'")
print("You can get the list of the words used by typing 'words'")
print("Please keep in mind that you cannot use special characters nor uppercase letters.")
print("_______________________________________________________________________________________")


def words():
    print(mots)
    return True


def test_word(w):
    lon = len(w)
    for i in range(0, lon):
        if w[i] in alphabet:
            i += 1
        else:
            print("Nope, You cannot use special characters")
            return False
    return True


def end(dernier):
    mots.clear()
    print("")
    print("")
    print("Do you want to play again?")
    print("1: Yes")
    b = int(input("2: No"))
    if b == 1:
        print("--------------", dernier)
        return True
    if b == 2:
        exit()
    else:
        end(dernier)


t = 1
preum = alphabet[randint(0, 26)]
print("First letter: ", preum)
mots = []
der = []
dernier = None
points = 0
turn = 1

while len(mots) < 5:
    x = input("")
    y = x
    pr = x[0]

    if y == "stop":
        exit()

    if dernier is None:
        dernier = preum

    if test_word(x):
        if len(y) == 1:
            print("Wrong, only one letter....")
            print("Game over!! Not enough letters!")
            print("Number of turns: ", turn, "    Points: ", points)
            points = 0
            lon = len(x)
            for i in range(lon):
                if x[i] is "y":
                    points -= 10
                if x[i] in voyelles:
                    points -= 3
                if x[i] in cons:
                    points -= 1
            turn = 1
            end(dernier)

        if len(y) >= 2:
            if y in mots:
                print("Game over!! Word already used!")
                print("Number of turns: ", turn, "    Points: ", points)
                points = 0
                lon = len(x)
                for i in range(lon):
                    if x[i] is "y":
                        points -= 10
                    if x[i] in voyelles:
                        points -= 3
                    if x[i] in cons:
                        points -= 1
                turn = 1
                end(dernier)
            if dernier != pr:
                print("Game over!! Wrong first letter!")
                print("Number of turns: ", turn, "    Points: ", points)
                points = 0
                lon = len(x)
                for i in range(lon):
                    if x[i] is "y":
                        points -= 10
                    if x[i] in voyelles:
                        points -= 3
                    if x[i] in cons:
                        points -= 1
                turn = 1
                end(dernier)
            else:
                lon = len(x)
                for i in range(lon):
                    if x[i] is "y":
                        points += 10
                    if x[i] in voyelles:
                        points += 3
                    if x[i] in cons:
                        points += 1
                mots.append(str(y))
                turn += 1
                dernier = y[-1]
                print(y, " -----", dernier, "                                                         Points: ", points)

print("")
print("Maximum de points: ", points)







