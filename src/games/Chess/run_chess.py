## Code Cleaned Up ##

import ctypes
import sys as system
import threading
from time import sleep
from tkinter import messagebox

from src import run_main
from src.games.Chess.Chess import *
from src.resources.utils.Constants import Constants as Ct, ImgLoader as Il


#####          STATIC METHODS          ####
# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V5.2")
####                                  ####


class ChessGui:

    def __init__(self):
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Chess - Alpha V6.0")
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
        myappid = 'mjcorp.Chess.alphav6.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Chess\\taskbar.ico'))
        ImgLoader = Il()

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        self.create_menubar(menubar)

        chess_array_img = ImgLoader.load_img('resources\\images\\Chess\\ChessPiecesArray.png')

        whites = {'Pawn': ImgLoader.resize_img(chess_array_img.crop((300, 60, 360, 120)), (52, 52)),
                  'King': ImgLoader.resize_img(chess_array_img.crop((60, 60, 120, 120)), (52, 52)),
                  'Queen': ImgLoader.resize_img(chess_array_img.crop((0, 60, 60, 120)), (52, 52)),
                  'Tower': ImgLoader.resize_img(chess_array_img.crop((120, 60, 180, 120)), (52, 52)),
                  'Bishop': ImgLoader.resize_img(chess_array_img.crop((240, 60, 300, 120)), (52, 52)),
                  'Knight': ImgLoader.resize_img(chess_array_img.crop((180, 60, 240, 120)), (52, 52))}
        blacks = {'Pawn': ImgLoader.resize_img(chess_array_img.crop((300, 0, 360, 60)), (52, 52)),
                  'King': ImgLoader.resize_img(chess_array_img.crop((60, 0, 120, 60)), (52, 52)),
                  'Queen': ImgLoader.resize_img(chess_array_img.crop((0, 0, 60, 60)), (52, 52)),
                  'Tower': ImgLoader.resize_img(chess_array_img.crop((120, 0, 180, 60)), (52, 52)),
                  'Bishop': ImgLoader.resize_img(chess_array_img.crop((240, 0, 300, 60)), (52, 52)),
                  'Knight': ImgLoader.resize_img(chess_array_img.crop((180, 0, 240, 60)), (52, 52))}
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

        self.b_class.pass_board_to_pieces()

        self.root.mainloop()

    def start_game(self):
        self.playing = True
        self.t1 = threading.Thread(target=self.update_timer, args=())
        self.t1.start()
        self.start_button.config(text='Pause', command=self.pause_game)
        self.update_board()

    def pause_game(self):
        self.playing = False
        self.start_button.config(text='Resume', command=self.start_game)
        self.hide_board()

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
        print('switched players\n')

    def clicked(self, button):
        if not self.playing:
            return
        print('----------------------------')
        board = self.b_class.board
        curr_pos = Position([button.grid_info()['column'], button.grid_info()['row']])
        piece_clicked_on = board[curr_pos.y][curr_pos.x]

        if button == self.last_button_clicked:
            self.last_piece = None
            self.last_button_clicked['bg'] = self.last_color
            self.last_color = ''
            self.last_button_clicked = None
            print('last clicked')
            return

        if self.last_piece is None:
            if piece_clicked_on is None:
                return
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

        if curr_pos.get_position() in [pos.get_position() for pos in self.last_piece.get_valid_positions()]:
            if not self.b_class.move_piece_to(self.last_piece, curr_pos):
                print(f'unable to move piece to {curr_pos.get_position()}')
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
            self.switch_players()
            if self.b_class.check_for_checks(self.player):
                _over = self.b_class.check_over(self.player)
                print(f'over: {_over}')
                if _over:
                    self.switch_players()
                    print(f'Player {self.player+1} won!')
                    self._over()
            return

        print(curr_pos.get_position(), '--', [pos.get_position() for pos in self.last_piece.get_valid_positions()])

        if self.b_class.get(curr_pos.x, curr_pos.y) is None:
            print('b_çclass.get() is None')
            return

        if self.b_class.get(curr_pos.x, curr_pos.y).get_color() == self.last_piece.get_color():
            self.last_button_clicked['bg'] = self.last_color

            self.last_piece = piece_clicked_on
            self.last_color = button['bg']
            button['bg'] = 'blue'
            self.last_button_clicked = button
            self.last_position = Position([curr_pos.x, curr_pos.y])
            print('same team dude')
            return

    def update_board(self):
        board = self.b_class.return_board()
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > 7:
                return
            piece: ChessPiece = board[b['row']][b['column']]
            button['image'] = ''
            button['bg'] = self.color_pattern[b['row']][b['column']]
            if piece is not None:
                button['image'] = self.images.get(piece.get_color()).get(piece.get_type())
                if isinstance(piece, King) and piece.is_checked():
                    button['bg'] = 'red'

    def hide_board(self):
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > 7:
                return
            button['image'] = ''

    def _over(self):
        for button in Ct.all_children(self.root, 'Button'):
            button['command'] = ''
        self.playing = False

    def change_color(self, color1, color2):
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > 7:
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
    ChessGui()
