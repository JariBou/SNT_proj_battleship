import ctypes
import threading
import time
import tkinter as tk
from PIL.ImageTk import PhotoImage
from tkinter import font as ft, messagebox

from src.games.Chess import run_chess
from src.resources.utils.Constants import Constants
from src import run_main


#####          STATIC METHODS          ####
def g_help():
    messagebox.showinfo(title="Help & Rules",
                        message="Speed float is given as 1 over the number of squares it moves per second\n"
                                "(1 / 0.075 ~ 13.33squares/sec)")   ##TODO: help function ya know it


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari & Mathis \n "
                                               "Version: Alpha 2.1")


####                                  ####


class Launcher:

    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Chess Launcher")
        menubar = tk.Menu(self.w)
        self.w.config(menu=menubar)
        self.create_menu(menubar)
        myappid = 'mjcorp.chessl.alphav2.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Constants.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\Chess\\taskbar.ico'))

        self.board_size = tk.StringVar(value='[8, 8]')
        self.variant_name = tk.StringVar(value='None')

        customFont = ft.Font(family='Source Sans Pro Black', size=17)
        customFont_radio = ft.Font(family='Source Sans Pro Black', size=14)
        self.running = True
        imgs = {'icon': PhotoImage(file=self.path.joinpath('resources\\images\\Chess\\taskbar_img_2.png'))}
        tk.Label(self.w, borderwidth=10, relief="ridge", image=imgs['icon'], font=customFont).grid(row=0, column=0, sticky='n')

        self.args_frame = tk.Frame(self.w, borderwidth=6, relief="groove")
        tk.Label(self.args_frame, text='Board size: ', font=customFont).grid(row=0, column=0, sticky='w')
        tk.OptionMenu(self.args_frame, self.board_size, '[8, 8]', '[5, 6]', '[4, 5]', '[5, 5]', '[6, 6]').grid(row=0, column=1)
        tk.Label(self.args_frame, text='Variant name: ', font=customFont).grid(row=1, column=0, sticky='w')
        tk.OptionMenu(self.args_frame, self.variant_name, '').grid(row=1, column=1)
        self.args_frame.columnconfigure(1, minsize=150)
        self.args_frame.grid(row=1, column=0, rowspan=2)

        tk.Button(self.w, text='Open Chess',
                  command=self.chess, font=customFont, relief=tk.RAISED, border=10).grid(row=5, column=0, columnspan=2)

        self.t1 = threading.Thread(target=self.loop)
        self.t1.start()

        self.color_frame = tk.Frame(self.w, borderwidth=6, relief="solid")
        self.color_var = tk.StringVar()
        self.color_var.set("[black, white]")
        tk.Label(self.color_frame, text='--Colors--', font=customFont).pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame, text='Black & White', font=customFont_radio, variable=self.color_var,
                                value="[black, white]")
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame, text='Terracota & Ivory', font=customFont_radio, variable=self.color_var,
                                value="[brown, ivory]")
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame, text='Gold & Ivory', font=customFont_radio, variable=self.color_var,
                                value="[gold, ivory]")
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame, text='Dark brown & Ivory', font=customFont_radio, variable=self.color_var,
                                value="[#662200, ivory]")
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame, text='Dark turquoise & Light blue', font=customFont_radio,
                                variable=self.color_var, value="[#006666, #809fff]")
        radio5.pack(anchor='nw', padx=30)
        radio6 = tk.Radiobutton(self.color_frame, text='Black & Orange', font=customFont_radio,
                                variable=self.color_var, value="[black, #ff9933]")
        radio6.pack(anchor='nw', padx=30)
        self.color_frame.grid(row=0, column=1, rowspan=2)

        self.w.columnconfigure(0, minsize=200)
        Constants.center(self.w)
        self.prev_val = ''

        self.w.mainloop()

    def loop(self):
        while self.running:
            size = self.board_size.get()
            if self.prev_val == size:
                continue
            elif size == '[8, 8]' or size == '[6, 6]':
                tk.OptionMenu(self.args_frame, self.variant_name, 'None').grid(row=1, column=1)
                self.variant_name.set('None')
            elif size == '[5, 6]':
                tk.OptionMenu(self.args_frame, self.variant_name, 'Chess attack', 'Speed chess', 'Elena chess').grid(row=1, column=1)
                self.variant_name.set('Chess attack')
            elif size == '[4, 5]':
                tk.OptionMenu(self.args_frame, self.variant_name, 'Microchess', 'Silverman 4×5').grid(row=1, column=1)
                self.variant_name.set('Microchess')
            elif size == '[5, 5]':
                tk.OptionMenu(self.args_frame, self.variant_name, 'Baby chess', 'Jacobs–Meirovitz', 'Gardner').grid(row=1, column=1)
                self.variant_name.set('Baby chess')
            self.prev_val = self.board_size.get()
            time.sleep(0.1)

    def chess(self):
        self.running = False
        if self.t1 is not None:
            self.t1.join(timeout=0.5)
        self.w.destroy()
        run_chess.ChessGui(board_size=Constants.convert_str_to_list(self.board_size.get()),
                           variant_name=self.variant_name.get(),
                           color=Constants.convert_str_to_list(self.color_var.get()))

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])


if __name__ == '__main__':
    Launcher()
