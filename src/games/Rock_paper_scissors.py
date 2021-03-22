from pathlib import Path
from tkinter import *
import random as r
from src.resources.utils.Constants import Constants as ct


class Game:

    def __init__(self):
        self.w = Tk()
        self.w.geometry("700x500")
        self.w.title("Window")
        self.result = Label(self.w, text='')
        self.result.grid(row=1, column=1)
        self.path = Path(__file__).parent.parent

        humain = Label(text="Humain:")
        humain.grid(row=0, column=0)
        humain = Label(text="Machine:")
        humain.grid(row=0, column=2)

        img4 = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\rien.png"))
        self.rien = img4
        self.voidH = Label(image=img4)
        self.voidH.grid(row=2, column=0)
        self.voidCPU = Label(image=img4)
        self.voidCPU.grid(row=2, column=2)

        self.machineP = Label(text="0")
        self.machineP.grid(row=1, column=2)
        self.humainP = Label(text="0")
        self.humainP.grid(row=1, column=0)

        # Pierre               #Feuille            #Ciseaux             #Lezard            #Spock
        self.list = [[0, -1, 1, 1, -1], [1, 0, -1, -1, 1], [-1, 1, 0, 1, -1], [-1, 1, -1, 0, 1], [1, -1, 1, -1, 0]]

        self.cpuWin = 0
        self.pWin = 0
        self.w.grid_columnconfigure(4, minsize=100)
        self.pierre = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\pierre.png"))
        self.papier = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\feuille.png"))
        self.ciseaux = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\ciseaux.png"))
        self.lezard = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\lezard.png"))
        self.spockImg = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\spock.png"))
        self.image_list = [self.pierre, self.papier, self.ciseaux, self.lezard, self.spockImg]

        img_nb = 0
        for row in range(4, 6):
            for column in range(0, 3):
                if row == 5 and column == 2:
                    break
                img = self.image_list[img_nb]
                print(img_nb)
                Button(self.w, image=img, command=lambda value=img_nb, image=img: self.choice(image, value)).grid(row=row, column=column)
                img_nb += 1

        text = Label(text="Pour jouer appuyez sur un bouton:")
        text.grid(row=3, columnspan=3)

        img3 = PhotoImage(file=self.path.joinpath("resources\\images\\rock_paper_scissors\\versus.gif"))
        versus = Label(image=img3)
        versus.grid(row=2, column=1)

        resetButton = Button(text="Reset Game", command=self.resetC)
        resetButton.grid(row=3, column=6)
        self.w.mainloop()

    def CPU(self, player):
        cpu = r.randint(0, 4)
        self.change(cpu)
        result = self.list[player][cpu]
        self.pWin += result if result != -1 else 0
        self.cpuWin += -result if result != 1 else 0
        self.draw()
        if result == 0:
            self.result.config(text='Egalité!')
        elif result == 1:
            self.result.config(text='Gagné!')
        else:
            self.result.config(text='Perdu...')

    def choice(self, img, play_value):
        self.voidH.config(image=img)
        self.CPU(play_value)

    def change(self, number):
        self.voidCPU.config(image=self.image_list[number])

    def draw(self):
        self.machineP.config(text=str(self.cpuWin))
        self.humainP.config(text=str(self.pWin))

    def resetC(self):
        self.pWin = 0
        self.cpuWin = 0
        self.result.config(text="")
        self.voidCPU.config(image=self.rien)
        self.voidH.config(image=self.rien)
        self.draw()


a = Game()
