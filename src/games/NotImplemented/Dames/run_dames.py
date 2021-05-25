## Code Cleaned Up ##

import ctypes
import sys as system
import threading
from time import sleep
from tkinter import messagebox
import tkinter as tk

from src import run_main
from src.games.NotImplemented.Dames.Pieces import *
from src.resources.utils.Constants import Constants as Ct, ImgLoader as Il


#####          STATIC METHODS          ####
# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V1.0")
####                                  ####


class DamesGui:

    def __init__(self):
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Chess - Dames V1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        w = 800
        h = 800
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ## Add Icon
        myappid = 'mjcorp.Dames.alphav1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.board_size = 8

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        self.create_menubar(menubar)

        for i in range(0, 8):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=75)

        self.defaultbg = self.root.cget('bg')

        self.b_class = Board()
        board = self.b_class.board

        self.buttons_list = []
        self.color_pattern = []
        ImgLoader = Il()
        chess_array_img = ImgLoader.load_img('resources\\images\\Chess\\ChessPiecesArray.png')
        self.images = {'White':ImgLoader.resize_img(chess_array_img.crop((300, 60, 360, 120)), (52, 52)),
                       'Black':ImgLoader.resize_img(chess_array_img.crop((300, 0, 360, 60)), (52, 52))}

        for row in range(0, self.board_size):
            for column in range(0, self.board_size):
                bg = 'black' if (column + row) % 2 == 0 else 'white'
                a = tk.Button(self.root, bg=bg, activebackground='lightblue')
                piece = board[row][column]
                try:
                    a['image'] = self.images.get(piece.get_color())
                except AttributeError:
                    pass
                a["command"] = lambda a1=a: self.clicked(a1)
                a.grid(row=row, column=column, sticky='nsew')
                self.buttons_list.append(a)
                self.color_pattern.append(a['bg'])

        self.buttons_list = Ct.regroup_list(self.buttons_list, 8)
        self.logic_color = [1 if self.color_pattern[i] == 'black' else 0 for i in range(len(self.color_pattern))]
        self.color_pattern = Ct.regroup_list(self.color_pattern, 8)
        self.logic_color = Ct.regroup_list(self.logic_color, 8)
        print(self.logic_color)

        self.playing = False
        self.player = 0
        self.colors = ['White', 'Black']

        self.s_round = 0
        self.p1_time = {'minutes': 0, 'seconds': 0}
        self.p2_time = {'minutes': 0, 'seconds': 0}
        self.time_dict = {'0': self.p1_time, '1': self.p2_time}
        self.curr_player = tk.Label(self.root, text=f'Current Player: {self.player + 1}  ({self.colors[self.player]})')
        self.curr_player.grid(row=0, column=8)
        self.timer = tk.Label(self.root, text='-timer-')
        self.timer.grid(row=1, column=8)

        self.switch_player = tk.Button(self.root, text='switch', command=self.switch_players)
        self.switch_player.grid(row=3, column=8)
        self.start_button = tk.Button(self.root, text='Start', command=self.start_game, relief=tk.RIDGE, border=10)
        self.start_button.grid(row=2, column=8, sticky='nsew')

        self.t1 = None

        self.last_button_clicked = None
        self.last_piece = None
        self.last_position = None
        self.last_color = ''
        self.check_last_color = ''
        self.in_path = False

        self.b_class.pass_board_to_pieces()

        self.root.mainloop()

    def start_game(self):
        self.playing = True
        self.t1 = threading.Thread(target=self.update_timer, args=())
        self.t1.start()
        self.start_button.config(text='Pause', command=self.pause_game)
        #self.update_board()

    def pause_game(self):
        self.playing = False
        self.start_button.config(text='Resume', command=self.start_game)
        #self.hide_board()

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
        sleep(0.5)
        system.exit('User cancelation')

    def switch_players(self):
        self.player = 1 if self.player == 0 else 0
        self.curr_player.config(text=f'Current Player: {self.player + 1}  ({self.colors[self.player]})')
        print('switched players\n')

    def clicked(self, button):
        board = self.b_class.board
        curr_pos = Position([button.grid_info()['column'], button.grid_info()['row']])
        print(self.last_piece)
        if self.in_path:
            pass
        if self.last_piece:
            self.b_class.force_move_to(self.last_piece, curr_pos)
            self.last_piece = None
        else:
            self.last_piece = board[curr_pos.y][curr_pos.x]
        self.update_board()
        pass

    def update_board(self):
        for button in Ct.all_children(self.root, 'Button'):
            b_info = button.grid_info()
            if b_info['row'] >= self.board_size or b_info['column'] >= self.board_size:
                return
            button['image'] = ''
            piece = self.b_class.board[b_info['row']][b_info['column']]
            if piece is not None:
                button['image'] = self.images.get(piece.get_color())

    def change_color(self, color1, color2):
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > self.board_size-1:
                return
            color = color1 if self.logic_color[b['column']][b['row']] == 1 else color2
            button['bg'], self.color_pattern[b['row']][b['column']] = color, color

    def create_menubar(self, menubar: tk.Menu):
        colorsettings = tk.Menu(menubar, tearoff=0)
        colorsettings.add_command(label="Black & White (default)", command=lambda: self.change_color('black', 'white'))
        colorsettings.add_command(label="Terracota & Ivory", command=lambda: self.change_color('brown', 'ivory'))
        colorsettings.add_command(label="Gold & Ivory", command=lambda: self.change_color('gold', 'ivory'))
        colorsettings.add_command(label="Dark brown & Ivory", command=lambda: self.change_color('#662200', 'ivory'))
        colorsettings.add_command(label="Dark turquoise & Light blue",
                                  command=lambda: self.change_color('#006666', '#809fff'))
        menubar.add_cascade(label="Board colors", menu=colorsettings)
        menubar.add_command(label="Help")  ##TODO: create help_rules window with rules
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


if __name__ == '__main__':
    DamesGui()
