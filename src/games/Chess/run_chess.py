import ctypes
import threading
import tkinter as tk
import sys as system
from time import sleep
from tkinter import messagebox
from PIL import ImageTk, Image
from threading import Timer

from src.resources.utils.Constants import Constants as Ct
from src.games.Chess.Chess import *


#####          STATIC METHODS          ####
def get_img(path):
    """ resources\\images\\XXX """
    img = Image.open(path)
    new_img = img.resize((52, 52))
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
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        w = 800
        h = 600
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ## Add Icon
        myappid = 'mjcorp.Chess.alphav0.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.iconbitmap(default=self.path.joinpath('resources\\images\\Chess\\taskbar.ico'))

        # self.root.overrideredirect(True)
        # self.root.lift()
        # self.root.wm_attributes("-topmost", True)
        # self.root.wm_attributes("-transparentcolor", "white")

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Help")  ##TODO: create help window with rules
        menubar.add_command(label="About", command=about)

        whites = {'Pawn': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Pawn.png'))}
        blacks = {'Pawn': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Pawn.png'))}
        self.images = {'White': whites, 'Black': blacks}

        for i in range(0, 8):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=75)

        self.defaultbg = self.root.cget('bg')

        b_class = Board()
        self.board = b_class.board

        for row in range(0, 8):
            for column in range(0, 8):
                bg = 'black' if (column + row) % 2 == 0 else 'white'
                a = tk.Button(self.root, bg=bg, activebackground='lightblue')
                piece = self.board[row][column]
                try:
                    a['image'] = self.images.get(piece.get_color()).get(piece.get_type())
                except AttributeError:
                    pass
                #a["command"] =
                a.grid(row=row, column=column, sticky='nsew')

        self.s_round = 0
        self.p1_time = {'minutes': 0, 'seconds': 0}
        self.p2_time = {'minutes': 0, 'seconds': 0}
        self.time_dict = {'0': self.p1_time, '1': self.p2_time}
        self.curr_player = tk.Label(self.root, text='hello')
        self.curr_player.grid(row=0, column=8)
        self.timer = tk.Label(self.root, text='hello')
        self.timer.grid(row=1, column=8)

        self.playing = True
        self.player = 0

        self.switch_player = tk.Button(self.root, text='switch', command=self.switch_players)
        self.switch_player.grid(row=2, column=8)

        self.t1 = None
        self.t1 = threading.Thread(target=self.update_timer, args=())
        self.t1.start()

        self.root.mainloop()

    def update_timer(self):
        while self.playing:
            sleep(0.25)
            if not self.playing:
                return
            self.s_round += 1
            curr = self.time_dict.get(str(self.player))
            if self.s_round == 2:
                curr['seconds'] += 0.5
                self.s_round = 0
            if curr['seconds'] >= 60:
                curr['minutes'] += 1
                curr['seconds'] = 0
            if not self.playing:
                return
            self.timer.config(text=f"{curr.get('minutes')}min {curr.get('seconds')}s")
            self.curr_player.config(text=f'Current Player: {self.player+1}')
        return

    def exit_game(self):
        self.playing = False
        cleanup_stop_thread()
        system.exit('User cancelation')
        self.t1.join()
        sleep(0.5)
        system.exit('User cancelation')

    def switch_players(self):
        self.player = 1 if self.player == 0 else 0
        print('switched players')


if __name__ == '__main__':
    a = Chess_Gui()
