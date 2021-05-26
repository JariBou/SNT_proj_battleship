import string
import threading
import tkinter as tk
from typing import Union


class GuiTests:

    def __init__(self):

        w = tk.Tk()
        w.title("tests")
        colormania = tk.BooleanVar()
        colormania.set(False)
        self.randomania = tk.BooleanVar(value=False)
        self.bapple = tk.BooleanVar(value=False)
        self.rando = tk.StringVar(value='[0, 5]')
        self.accelerato = tk.BooleanVar(value=False)
        self.acceleration = tk.DoubleVar(value=0.0075)
        self.speed = tk.DoubleVar(value=0.075)
        bapple_nb = tk.IntVar(value=3)
        self.columns = tk.IntVar(value=30)
        self.lines = tk.IntVar(value=30)
        self.square_size = tk.IntVar(value=10)
        self.running = True

        self.args_frame = tk.Frame(w)

        tk.Label(self.args_frame
                 , text='--Args--').grid(row=0, column=0, columnspan=2, sticky='n')
        tk.Checkbutton(self.args_frame, text='colormania', variable=colormania, anchor='w').grid(row=1, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='randomania', variable=self.randomania, anchor='w').grid(row=2, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='bapple', variable=self.bapple, anchor='w').grid(row=3, column=0, sticky='w')
        tk.Checkbutton(self.args_frame, text='accelerato', variable=self.accelerato, anchor='w').grid(row=4, column=0, sticky='w')
        tk.Label(self.args_frame, text='Base speed(advanced)', anchor='w').grid(row=5, column=0, sticky='w')
        self.rentry = tk.Entry(self.args_frame, textvariable=self.rando, state=tk.DISABLED)
        self.rentry.grid(row=1, column=1)
        self.bentry = tk.Entry(self.args_frame, textvariable=bapple_nb, state=tk.DISABLED)
        self.bentry.grid(row=2, column=1)
        self.accentry = tk.Entry(self.args_frame, textvariable=self.acceleration, state=tk.DISABLED)
        self.accentry.grid(row=3, column=1)
        tk.Entry(self.args_frame, textvariable=self.speed).grid(row=4, column=1)
        size_frame = tk.Frame(w)
        tk.Label(size_frame, text='columns: ', anchor='w').grid(row=0, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.columns).grid(row=0, column=1)
        tk.Label(size_frame, text='lines: ', anchor='w').grid(row=0, column=2, sticky='w')
        tk.Entry(size_frame, textvariable=self.lines).grid(row=0, column=3)
        tk.Label(size_frame, text='square length: ', anchor='w').grid(row=1, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.square_size).grid(row=1, column=1)
        tk.Button(w, text='print var',
                  command=lambda: print(convert_str_to_list(self.rando.get()))).grid(row=4, column=0)
        tk.Button(w, text='open snake',
                  command=lambda: self.snakeuh(w)).grid(row=5, column=0)
        size_frame.grid(row=1, column=0, columnspan=4)

        self.args_frame.grid(row=0, column=0)

        t1 = threading.Thread(target=self.loop)
        t1.start()

        ### pas du tout Ctrl + C  Ctrl + V
        self.color_frame = tk.Frame(w)

        self.color_var = tk.StringVar()
        self.color_var.set('modern')
        tk.Label(self.color_frame, text='--Colors--').pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame, text='Modern', variable=self.color_var,
                                value='modern')
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame, text='Vintage', variable=self.color_var,
                                value='vintage')
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame, text='Floor is lava', variable=self.color_var,
                                value='floorislava')
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame, text='Ocean', variable=self.color_var,
                                value='ocean')
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame, text='Outerworld',
                                variable=self.color_var, value='outerworld')
        radio5.pack(anchor='nw', padx=30)

        self.color_frame.grid(row=0, column=2)
        from src.resources.utils.Constants import Constants as Ct

        Ct.center(w)

        w.mainloop()

    def loop(self):
        while self.running:

            self.bentry.config(state=(tk.NORMAL if self.bapple.get() else tk.DISABLED))
            self.rentry.config(state=(tk.NORMAL if self.randomania.get() else tk.DISABLED))
            self.accentry.config(state=(tk.NORMAL if self.accelerato.get() else tk.DISABLED))

    def snakeuh(self, w):
        from src.games.Snake import Game
        w.destroy()
        Game(color=self.color_var.get())


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
    print(convert_str_to_list('[5, -5, hello,    -78, 4.5]'))
    g = 'a'
    a = [['a', '5'], ['b', '6'], ['c', '7']]
    b = ['a', '5']
    if g in a + b:
        print(g)
    print(a)
    print(b)
    GuiTests()
