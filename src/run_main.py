from tkinter import *
import tkinter.font as ft
from src.games.MorpionSolo import MorpionSolo
from src.games.MorpionMulti import MorpionMulti


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose GameMode")
        self.w.config(bg="lightgray")

        w = 700  # width for the Tk root
        h = 700  # height for the Tk root

        # get screen width and height
        ws = self.w.winfo_screenwidth()  # width of the screen
        hs = self.w.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.w.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.w.columnconfigure(0, minsize=130)
        self.w.columnconfigure(1, minsize=150)
        self.w.rowconfigure(0, minsize=150)

        customFont = ft.Font(size=20)

        # Set all buttons for apps
        size = 4
        buttonList = []

        morpion = Button(text="Morpion", command=self.morpion, font=customFont)
        buttonList.append(morpion)

        battleship = Button(text="Battleship", command='', font=customFont)
        buttonList.append(battleship)

        chess = Button(text="Chess", command='', font=customFont)
        buttonList.append(chess)

        gameoflife = Button(text="Jeu de la Vie", command='', font=customFont)
        buttonList.append(gameoflife)

        last_letter = Button(text="Dernière Lettre", command='', font=customFont)
        buttonList.append(last_letter)

        rockps = Button(text="Shifumi", command='', font=customFont)
        buttonList.append(rockps)

        lastgame = Button(text="???", command='', font=customFont)
        buttonList.append(lastgame)

        while len(buttonList) % size != 0:
            buttonList.append('None')

        buttonList = [buttonList[n:n + size + 1] for n in range(0, len(buttonList) + 1, size)]

        print(buttonList)
        exit_flag = False

        for row_index, row in enumerate(buttonList):
            print(row)
            if exit_flag:
                break
            for index, button in enumerate(row):
                if button == 'None':
                    exit_flag = True
                    break
                button.grid(row=row_index, column=index, sticky='nsew')

        self.w.mainloop()

    def morpion(self):
        self.w.destroy()

    def single(self):
        self.w.destroy()
        MorpionSolo()

    def multi(self):
        self.w.destroy()
        MorpionMulti()


if __name__ == '__main__':
    run()
