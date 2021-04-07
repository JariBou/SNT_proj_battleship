import ctypes
import math
import sys as system
import threading
import tkinter as tk
import random
from time import sleep

from src.resources.utils.Constants import Constants as Ct
from src.resources.utils.Constants import Position


#####          STATIC METHODS          ####
def place(button):
    button['bg'] = 'black' if button['bg'] == 'white' else 'white'
####                                  ####


class GameOfLife:

    def __init__(self):
        self.sw = tk.Tk()
        self.sw.title("Game Of Life - Alpha V0.1")
        self.sw.protocol("WM_DELETE_WINDOW", self.exit)
        self.label = tk.Label(self.sw, text='Enter the width of the grid (in number of squares)')
        self.label2 = tk.Label(self.sw, text='')
        self.entry_field = tk.Entry(self.sw)
        self.label.grid(row=0, column=0)
        self.label2.grid(row=2, column=0)
        self.entry_field.grid(row=1, column=0)
        self.ok_button = tk.Button(self.sw, text='confirm', command=self.confirm)
        self.ok_button.grid(row=1, column=1)
        self.width = 0
        self.height = 0

        self.sw.mainloop()

        self.root = tk.Tk()
        self.root.title("Game Of Life - Alpha V0.1")
        self.root.protocol("WM_DELETE_WINDOW", lambda: system.exit('User Cancelation'))
        self.root.attributes("-fullscreen", True)
        w = 700
        h = 500
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ## Add Icon
        myappid = 'mjcorp.gameoflife.alphav0.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()

        self.size = Position([self.width, self.height])    ## [X, Y]
        board = []
        for i in range(0, max(self.size.x, self.size.y)):
            self.root.rowconfigure(i, minsize=25)
            self.root.columnconfigure(i, minsize=25)

        self.t1 = None
        self.exit_flag = False

        self.first_start = True

        self.offsets = [Position([0, -1]), Position([1, 0]), Position([0, 1]), Position([-1, 0]),
                        Position([1, -1]), Position([1, 1]), Position([-1, -1]), Position([-1, 1])]

        for row in range(self.size.y):
            for column in range(self.size.x):
                a = tk.Button(self.root, bg='white')
                a['command'] = lambda but=a: place(but)
                a.grid(row=row, column=column, sticky='nsew')
                board.append(a)

        self.logic_board = [board[n:n + self.size.x+1] for n in range(0, len(board)+1, self.size.x)]

        self.start_button = tk.Button(self.root, text='Start', command=self.start)
        self.start_button.grid(row=0, column=self.size.x)

        self.quit_button = tk.Button(self.root, text='Quit', command=self.exit)
        self.quit_button.grid(row=0, column=self.size.x+1)

        self.restart_button = tk.Button(self.root, text='Restart', command=self.restart)
        self.restart_button.grid(row=0, column=self.size.x + 2)

        self.random_button = tk.Button(self.root, text='Random', command=self.randomise)
        self.random_button.grid(row=0, column=self.size.x + 3)

        self.root.mainloop()

    def start(self):
        self.random_button.config(state=tk.DISABLED)
        if self.first_start:
            for button in Ct.all_children(self.root, 'Button'):
                if button.grid_info()['column'] <= self.size.x:
                    button['command'] = ''
        self.first_start = False
        self.exit_flag = False
        self.t1 = threading.Thread(target=self.loop, args=()).start()
        self.start_button.config(text='Stop', command=self.stop)

    def stop(self):
        self.exit_flag = True
        self.start_button.config(text='Start', command=self.start)

    def loop(self):
        while True:
            if self.exit_flag:
                return
            to_die = []
            to_born = []
            for row in range(self.size.y):
                if self.exit_flag:
                    return
                for column in range(self.size.x):
                    count = 0
                    curr_cell = self.logic_board[row][column]
                    for offset in self.offsets:
                        try:
                            if self.logic_board[row+offset.y][column+offset.x]['bg'] == 'black':
                                count += 1
                        except IndexError:
                            pass
                    if (curr_cell['bg'] == 'white') and (count == 3):
                        to_born.append(self.logic_board[row][column])
                    elif (curr_cell['bg'] == 'black') and (count < 2 or count > 3):
                        to_die.append(self.logic_board[row][column])
            for button in to_die:
                button['bg'] = 'white'
            for button in to_born:
                button['bg'] = 'black'

    def restart(self):
        self.exit_flag = True

        self.root.destroy()
        GameOfLife()

    def confirm(self):
        try:
            self.width = int(self.entry_field.get())
            self.label.config(text='Enter the height of the grid (in number of squares)')
            self.ok_button['command'] = self.confirm2
            self.label2.config(text='')
        except ValueError:
            self.label2.config(text='Enter a Valid Integer')
        self.entry_field.delete(0, len(self.entry_field.get()))

    def confirm2(self):
        try:
            self.height = int(self.entry_field.get())
            self.sw.destroy()
        except ValueError:
            self.label2.config(text='Enter a Valid Integer')

    def randomise(self):
        for row in range(len(self.logic_board)):
            for column in range(len(self.logic_board[row])):
                if random.randint(0, 100) <= 10:
                    self.logic_board[row][column].config(bg='black')

    def exit(self):
        self.exit_flag = True
        try:
            self.t1.join()
        except AttributeError:
            pass
        system.exit('User Cancelation')


if __name__ == '__main__':
    GameOfLife()
