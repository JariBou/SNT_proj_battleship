## Code Cleaned Up ##

from src import run_main

from pathlib import Path
from tkinter import *
import random as r
import sys as system
from src.resources.utils.Constants import Constants as Ct

def g_help():
    message.showinfo(title= "Help", message = "C'est du morpion fréro")

def about():
    messagebox.showinfo(title="About", message="Made by: LeTiramissou & Jari\n "
                                               "Version: Alpha V1.0")

class Game:

    def __init__(self):
        w = Tk()
        w.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        ww = 800
        h = 500
        ## get screen width and height
        ws = w.winfo_screenwidth()
        hs = w.winfo_screenheight()
        ## calculate x and y coordinates for the window to be opened at
        x = (ws / 2) - (ww / 2)
        y = (hs / 2) - (h / 2)
        w.geometry('%dx%d+%d+%d' % (ww, h, x, y))
        w.title("Rock Paper Scissors Lizard Spock  -  Solo")

        self.result = Label(w, text='')
        self.result.grid(row=1, column=1)
        path = Path(__file__).parent.parent
        myappid = 'mjcorp.rockpaperscissors.alphav2.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\rock_paper_scissors\\icon.ico'))

        ## Create a Menubar
        menubar = Menu(w)
        w.config(menu=menubar)
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Game Select Menu", command=lambda: [w.destroy(), run_main.run_main()])

        humain = Label(text="Humain:")
        humain.grid(row=0, column=0)
        humain = Label(text="Machine:")
        humain.grid(row=0, column=2)

        img4 = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\rien.png"))
        self.rien = img4
        self.voidH = Label(image=img4)
        self.voidH.grid(row=2, column=0)
        self.voidCPU = Label(image=img4)
        self.voidCPU.grid(row=2, column=2)

        self.machineP = Label(text="0")
        self.machineP.grid(row=1, column=2)
        self.humainP = Label(text="0")
        self.humainP.grid(row=1, column=0)

        # Pierre             #Feuille           #Ciseaux           #Lezard           #Spock
        self.list = [[0, -1, 1, 1, -1], [1, 0, -1, -1, 1], [-1, 1, 0, 1, -1], [-1, 1, -1, 0, 1], [1, -1, 1, -1, 0]]

        self.cpuWin = 0
        self.pWin = 0
        w.grid_columnconfigure(4, minsize=100)
        pierre = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\pierre.png"))
        papier = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\feuille.png"))
        ciseaux = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\ciseaux.png"))
        lezard = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\lezard.png"))
        spockImg = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\spock.png"))
        self.image_list = [pierre, papier, ciseaux, lezard, spockImg]

        img_nb = 0
        for row in range(4, 6):
            for column in range(0, 3):
                if row == 5 and column == 2:
                    break
                img = self.image_list[img_nb]
                print(img_nb)
                Button(w, image=img, command=lambda value=img_nb, image=img: self.choice(image, value)).grid(row=row,
                                                                                                             column=column)
                img_nb += 1

        text = Label(text="Pour jouer appuyez sur un bouton:")
        text.grid(row=3, columnspan=3)

        img3 = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\versus.gif"))
        versus = Label(image=img3)
        versus.grid(row=2, column=1)

        resetButton = Button(text="Reset Game", command=self.resetG)
        resetButton.grid(row=0, column=1)

        help_text = Label(text="Récapitulatif des coups gagnants: ")
        help_text.grid(row=0, column=5)

        help_img = PhotoImage(file=path.joinpath("resources\\images\\rock_paper_scissors\\lizard_spock.png"))
        help = Label(image=help_img)
        help.grid(row=1, rowspan=4, column=5)

        w.mainloop()

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

    def resetG(self):
        self.pWin = 0
        self.cpuWin = 0
        self.result.config(text="")
        self.voidCPU.config(image=self.rien)
        self.voidH.config(image=self.rien)
        self.draw()


if __name__ == '__main__':
    Game()
