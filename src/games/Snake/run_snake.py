import ctypes
import threading
import tkinter as tk
from PIL.ImageTk import PhotoImage
from tkinter import font as ft, messagebox
from typing import Union
from src.resources.utils.Constants import Constants
from src import run_main


#####          STATIC METHODS          ####
def g_help():
    messagebox.showinfo(title="Help & Rules",
                        message="Speed float is given as 1 over the number of squares it moves per second\n"
                                "(1 / 0.075 ~ 13.33squares/sec)"
                        )


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari & Mathis \n "
                                               "Version: Alpha 2.1")


####                                  ####


class Launcher:

    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Snake Launcher")
        menubar = tk.Menu(self.w)
        self.w.config(menu=menubar)
        self.create_menu(menubar)
        myappid = 'mjcorp.snake.alphav2.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Constants.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\snake\\snake.ico'))

        self.colormania = tk.BooleanVar(value=False)
        self.randomania = tk.BooleanVar(value=False)
        self.bapple = tk.BooleanVar(value=False)
        self.accelerato = tk.BooleanVar(value=False)
        self.walls = tk.BooleanVar(value=False)
        self.rando = tk.StringVar(value='[0, 5]')
        self.acceleration = tk.DoubleVar(value=0.0055)
        self.speed = tk.DoubleVar(value=0.075)
        self.max_speed = tk.DoubleVar(value=0.01)
        self.bapple_nb = tk.IntVar(value=3)
        self.columns = tk.IntVar(value=30)
        self.lines = tk.IntVar(value=30)
        self.square_size = tk.IntVar(value=10)
        self.walls_nb = tk.IntVar(value=5)

        customFont = ft.Font(family='Source Sans Pro Black', size=17)
        self.running = True
        imgs = {'snake': PhotoImage(file=self.path.joinpath('resources\\images\\snake\\snake.png'))}

        tk.Label(self.w, text='Snake', image=imgs['snake'], font=customFont).grid(row=0, column=1, sticky='n')

        self.args_frame = tk.Frame(self.w)
        tk.Label(self.args_frame, text='--Args--', font=customFont).grid(row=0, column=0, columnspan=2, sticky='n')
        tk.Checkbutton(self.args_frame, text='colormania', font=customFont, variable=self.colormania, anchor='w').grid(
            row=1, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='randomania', font=customFont, variable=self.randomania, anchor='w').grid(
            row=2, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='bapple', font=customFont, variable=self.bapple, anchor='w').grid(row=3,
                                                                                                               column=0,
                                                                                                               sticky='w')
        tk.Checkbutton(self.args_frame, text='accelerato', font=customFont, variable=self.accelerato, anchor='w').grid(
            row=4, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='walls', font=customFont, variable=self.walls, anchor='w').grid(row=5,
                                                                                                             column=0,
                                                                                                             sticky='w')
        tk.Label(self.args_frame, text='Base speed(advanced)', font=customFont, anchor='w').grid(row=6, column=0,
                                                                                                 sticky='w')
        tk.Label(self.args_frame, text='Max speed(advanced)', font=customFont, anchor='w').grid(row=7, column=0,
                                                                                                sticky='w')

        self.rentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.rando, state=tk.DISABLED)
        self.rentry.grid(row=2, column=1)
        self.bentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.bapple_nb, state=tk.DISABLED)
        self.bentry.grid(row=3, column=1)
        self.accentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.acceleration, state=tk.DISABLED)
        self.accentry.grid(row=4, column=1)
        self.wentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.walls_nb, state=tk.DISABLED)
        self.wentry.grid(row=5, column=1)
        tk.Entry(self.args_frame, font=customFont, textvariable=self.speed).grid(row=6, column=1)
        tk.Entry(self.args_frame, font=customFont, textvariable=self.max_speed).grid(row=7, column=1)
        self.args_frame.grid(row=0, column=0, rowspan=2)

        size_frame = tk.Frame(self.w)
        tk.Label(size_frame, text='Size:', font=customFont, anchor='w').grid(row=0, column=0, sticky='w')
        tk.Label(size_frame, text='columns: ', font=customFont, anchor='w').grid(row=1, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.columns, font=customFont).grid(row=1, column=1)
        tk.Label(size_frame, text='lines: ', font=customFont, anchor='w').grid(row=1, column=2, sticky='w')
        tk.Entry(size_frame, textvariable=self.lines, font=customFont).grid(row=1, column=3)
        tk.Label(size_frame, text='square length: ', font=customFont, anchor='w').grid(row=2, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.square_size, font=customFont).grid(row=2, column=1)
        size_frame.grid(row=2, column=0, columnspan=4)

        tk.Button(self.w, text='Open snake',
                  command=self.snakeuh, font=customFont, relief=tk.RAISED, border=10).grid(row=5, column=0, columnspan=2)

        self.t1 = threading.Thread(target=self.loop)
        self.t1.start()

        ### pas du tout Ctrl + C  Ctrl + V
        self.color_frame = tk.Frame(self.w)
        self.color_var = tk.StringVar()
        self.color_var.set('modern')
        tk.Label(self.color_frame, text='--Colors--', font=customFont).pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame, text='Modern', font=customFont, variable=self.color_var,
                                value='modern')
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame, text='Vintage', font=customFont, variable=self.color_var,
                                value='vintage')
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame, text='Floor is lava', font=customFont, variable=self.color_var,
                                value='floorislava')
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame, text='Ocean', font=customFont, variable=self.color_var,
                                value='ocean')
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame, text='Outerworld', font=customFont,
                                variable=self.color_var, value='outerworld')
        radio5.pack(anchor='nw', padx=30)

        self.color_frame.grid(row=1, column=1)
        from src.resources.utils.Constants import Constants as Ct

        Ct.center(self.w)

        self.w.mainloop()

    def loop(self):
        while self.running:
            self.bentry.config(state=(tk.NORMAL if self.bapple.get() else tk.DISABLED))
            self.rentry.config(state=(tk.NORMAL if self.randomania.get() else tk.DISABLED))
            self.accentry.config(state=(tk.NORMAL if self.accelerato.get() else tk.DISABLED))
            self.wentry.config(state=(tk.NORMAL if self.walls.get() else tk.DISABLED))

    def snakeuh(self):
        from src.games.Snake.Snake import Game
        self.running = False
        self.w.destroy()
        Game(color=self.color_var.get(),
             randomania=self.randomania.get(),
             rando_range=convert_str_to_list(self.rando.get()),
             bapple=self.bapple.get(),
             nb_bapple=self.bapple_nb.get(),
             accelerato=self.accelerato.get(),
             acceleration=self.acceleration.get(),
             walls=self.walls.get(),
             nb_walls=self.walls_nb.get(),
             colormania=self.colormania.get(),
             speed=self.speed.get(),
             nb_columns=self.columns.get(),
             nb_lines=self.lines.get(),
             square_dim=self.square_size.get(),
             max_speed=self.max_speed.get())

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])


def convert_str_to_list(str_list: str) -> list[Union[float, str]]:
    str_list.strip()
    if not (str_list[0] == '[' and str_list[len(str_list) - 1] == ']'):
        raise ValueError(f'Cannot convert {str_list} to list')
    values = str_list[1:-1].split(',')
    L = []
    for val in values:
        try:
            L.append(float(val))
        except ValueError:
            L.append(val.strip())
    return L


if __name__ == '__main__':
    Launcher()
