import ctypes
import random
import sys as system
import threading
import tkinter as tk

from tkinter import messagebox
from src import run_main
from src.resources.utils.Constants import Constants as Ct, Position


#####          STATIC METHODS          ####
def place(button):
    button['bg'] = 'black' if button['bg'] == 'white' else 'white'

def g_help():
    messagebox.showinfo(title = "Help & Rules", message="Une cellule possède huit voisins, qui sont les cellules adjacentes horizontalement, verticalement et diagonalement.\n\n"
    "À chaque étape, l’évolution d’une cellule est déterminée par l’état de ses huit voisines de la façon suivante :\n\n"
    "* Une cellule morte possédant exactement trois voisines vivantes devient vivante (elle naît)\n"
    "* une cellule vivante possédant deux ou trois voisines vivantes le reste, sinon elle meurt")

def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V3.0")


####                                  ####


class GameOfLife:

    def __init__(self):
        self.sw = tk.Tk()
        self.sw.title("Game Of Life - Alpha V3.0")
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

        self.sw.bind("<Return>", self.on_key_press)

        self.sw.mainloop()

        self.root = tk.Tk()
        self.root.title("Game Of Life - Alpha V3.0")
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
        myappid = 'mjcorp.gameoflife.alphav3.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])

        self.size = Position([self.width, self.height])  ## [X, Y]
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

        self.logic_board = [board[n:n + self.size.x + 1] for n in range(0, len(board) + 1, self.size.x)]

        self.start_button = tk.Button(self.root, text='Start', command=self.start)
        self.start_button.grid(row=0, column=self.size.x)

        self.quit_button = tk.Button(self.root, text='Quit', command=self.exit)
        self.quit_button.grid(row=0, column=self.size.x + 1)

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
                            if self.logic_board[row + offset.y][column + offset.x]['bg'] == 'black':
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
            self.sw.bind('<Return>', self.confirm2)
            self.label2.config(text='')
        except ValueError:
            self.label2.config(text='Enter a Valid Integer')
        self.entry_field.delete(0, len(self.entry_field.get()))

    def confirm2(self, args=0):
        if args:   # otherwise error with enter keybind
            print(args)
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

    def on_key_press(self, event):
        key_pressed = repr(event.char).replace("'", '', 2)
        key_pressed = str(key_pressed)
        if key_pressed == '\\r':  # Enter key
            if self.width:
                self.confirm2()
            else:
                self.confirm()


if __name__ == '__main__':
    GameOfLife()
