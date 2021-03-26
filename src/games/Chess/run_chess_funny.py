import ctypes
import tkinter as tk
import sys as system
from tkinter import messagebox
from PIL import ImageTk, Image

from src.resources.utils.Constants import Constants as Ct

from src.games.Chess.Chess import *


#####          STATIC METHODS          ####
def get_img(path):
    """ resources\\images\\XXX """
    img = Image.open(path)
    new_img = img.resize((44, 44))
    photo = ImageTk.PhotoImage(new_img)
    return photo


# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V0.1")
    ####                                  ####


class Chess_Gui:

    def __init__(self):
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Chess - Alpha V0.1")
        self.root.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.width, self.height = screen_width / 1.25, screen_height / 1.25
        ## calculate x and y coordinates for the window to be opened at
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        ## Add Icon
        myappid = 'mjcorp.Chess.alphav0.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.iconbitmap(default=self.path.joinpath('resources\\images\\Chess\\taskbar.ico'))

        self.root.overrideredirect(True)
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Help")  ##TODO: create help window with rules
        menubar.add_command(label="About", command=about)

        self.image = {'Test_Pawn': get_img(self.path.joinpath('resources\\images\\Chess\\taskbar.png'))}

        for i in range(0, 9):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=75)

        self.defaultbg = self.root.cget('bg')

        for column in range(0, 9):
            for row in range(0, 9):
                bg = 'black' if (column + row) % 2 == 0 else 'white'
                a = tk.Button(self.root, bg=bg, activebackground='lightblue', image=self.image.get('Test_Pawn'))
                #a["command"] =
                a.grid(row=row, column=column, sticky='nsew')

        self.root.mainloop()


if __name__ == '__main__':
    a = Chess_Gui()
