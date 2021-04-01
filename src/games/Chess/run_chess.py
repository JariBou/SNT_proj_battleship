import ctypes
import threading
import tkinter as tk
import sys as system
from time import sleep
from tkinter import messagebox
from PIL import ImageTk, Image

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


class ChessGui:

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

        whites = {'Pawn': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Pawn.png')),
                  'King': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\King.png')),
                  'Queen': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Queen.png')),
                  'Tower': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Tower.png')),
                  'Bishop': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Bishop.png')),
                  'Knight': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\White\\Knight.png'))}
        blacks = {'Pawn': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Pawn.png')),
                  'King': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\King.png')),
                  'Queen': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Queen.png')),
                  'Tower': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Tower.png')),
                  'Bishop': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Bishop.png')),
                  'Knight': get_img(self.path.joinpath('resources\\images\\Chess\\Pieces\\Black\\Knight.png'))}
        self.images = {'White': whites, 'Black': blacks}

        for i in range(0, 8):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=75)

        self.defaultbg = self.root.cget('bg')

        self.b_class = Board()
        board = self.b_class.board

        self.buttons_list = []
        self.color_pattern = []

        for row in range(0, 8):
            for column in range(0, 8):
                bg = 'black' if (column + row) % 2 == 0 else 'white'
                a = tk.Button(self.root, bg=bg, activebackground='lightblue')
                piece = board[row][column]
                try:
                    a['image'] = self.images.get(piece.get_color()).get(piece.get_type())
                except AttributeError:
                    pass
                a["command"] = lambda a=a: self.clicked(a)
                a.grid(row=row, column=column, sticky='nsew')
                self.buttons_list.append(a)
                self.color_pattern.append(a['bg'])

        print(self.color_pattern)
        print(len(self.color_pattern))
        self.buttons_list = Ct.regroup_list(self.buttons_list, 8)
        self.color_pattern = Ct.regroup_list(self.color_pattern, 8)

        self.playing = True
        self.player = 0
        self.colors = ['White', 'Black']

        self.s_round = 0
        self.p1_time = {'minutes': 0, 'seconds': 0}
        self.p2_time = {'minutes': 0, 'seconds': 0}
        self.time_dict = {'0': self.p1_time, '1': self.p2_time}
        self.curr_player = tk.Label(self.root, text=f'Current Player: {self.player + 1}  ({self.colors[self.player]})')
        self.curr_player.grid(row=0, column=8)
        self.timer = tk.Label(self.root, text='hello')
        self.timer.grid(row=1, column=8)

        self.switch_player = tk.Button(self.root, text='switch', command=self.switch_players)
        self.switch_player.grid(row=2, column=8)

        self.t1 = None
        self.t1 = threading.Thread(target=self.update_timer, args=())
        self.t1.start()

        self.last_button_clicked = None
        self.last_piece = None
        self.last_position = None
        self.last_color = ''
        self.check_last_color = ''

        self.b_class.pass_board_to_pieces()

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
        return

    def exit_game(self):
        self.playing = False
        self.t1.join()
        sleep(0.5)
        system.exit('User cancelation')

    def switch_players(self):
        self.player = 1 if self.player == 0 else 0
        self.curr_player.config(text=f'Current Player: {self.player + 1}  ({self.colors[self.player]})')
        print('switched players')

    def clicked(self, button):
        print('----------------------------')
        board = self.b_class.board
        curr_pos = Position([button.grid_info()['column'], button.grid_info()['row']])
        piece_clicked_on = board[curr_pos.y][curr_pos.x]

        if button == self.last_button_clicked:
            self.last_piece = None
            self.last_button_clicked['bg'] = self.last_color
            self.last_color = ''
            self.last_button_clicked = None
            return

        if self.last_piece is None and piece_clicked_on is not None:
            for p, color in zip([0, 1], ['Black', 'White']):
                try:
                    if self.player == p and piece_clicked_on.get_color() == color:
                        print(f'Wrong color: player{self.player} clicked on {color} piece')
                        return
                except AttributeError:
                    pass
            self.last_piece = piece_clicked_on
            self.last_color = button['bg']
            button['bg'] = 'blue'
            self.last_button_clicked = button
            self.last_position = Position([curr_pos.x, curr_pos.y])
            return

        if self.last_piece is None:
            return

        if curr_pos.get_position() in [pos.get_position() for pos in self.last_piece.get_valid_positions()]:
            if not self.b_class.move_piece_to(self.last_piece, curr_pos):
                return
            self.last_button_clicked['bg'] = self.last_color
            if isinstance(self.last_piece, Pawn) and self.last_piece.reached_end():
                self.update_board()
                self.last_piece.transform()
                self.b_class.pass_board_to_pieces()
            self.update_board()
            self.last_color = ''
            self.last_piece = None
            self.last_button_clicked = None
            self.b_class.print_board()
            self.switch_players()

    def update_board(self):
        board = self.b_class.return_board()
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > 7:
                return
            piece = board[b['row']][b['column']]
            button['image'] = ''
            button['bg'] = self.color_pattern[b['row']][b['column']]
            if piece is not None:
                button['image'] = self.images.get(piece.get_color()).get(piece.get_type())
                if isinstance(piece, King) and piece.is_checked():
                    button['bg'] = 'red'


if __name__ == '__main__':
    a = ChessGui()
