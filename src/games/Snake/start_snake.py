## Code Cleaned Up ##
import ctypes
from tkinter import *
import tkinter.font as ft

from src import run_main
from src.games.GameOfLife import GameOfLife, GameOfLifeV2, GameOfLifeV3
from src.games.Snake import run_snake, run_snake2P
from src.resources.utils.Constants import Constants as Ct, Constants


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose number of players")
        self.w.config(bg="lightgray")

        ## Create a Menubar
        menubar = Menu(self.w)
        self.w.config(menu=menubar)
        self.w.resizable(width=False, height=False)
        myappid = 'mjcorp.snakelaucher.alphav1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Constants.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\snake\\snake.ico'))
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])

        customFont = ft.Font(size=20)
        P1 = Button(text="1 Player", command=lambda: (self.w.destroy(), run_snake.Launcher()), font=customFont)
        P1.grid(row=0, column=0, sticky="nsew")
        P2 = Button(text="2 Players", command=lambda: (self.w.destroy(), run_snake2P.Launcher()), font=customFont)
        P2.grid(row=0, column=1, sticky="nsew")

        Ct.center(self.w)
        w = self.w.winfo_width()
        h = self.w.winfo_height()
        print(w)
        for i in range(2):
            self.w.columnconfigure(i, minsize=round(w / 2))
        self.w.rowconfigure(0, minsize=h)
        Ct.center(self.w)

        self.w.mainloop()


if __name__ == '__main__':
    run()
