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
        self.randomania = tk.BooleanVar()
        self.randomania.set(False)
        self.bapple = tk.BooleanVar()
        self.bapple.set(False)
        self.rando = tk.StringVar()
        self.rando.set('[0, 5]')
        bapple_nb = tk.IntVar()
        bapple_nb.set(3)
        self.running = True

        self.args_frame = tk.Frame(w)

        tk.Checkbutton(self.args_frame, text='colormania', variable=colormania).grid(row=0, column=0)
        tk.Checkbutton(self.args_frame, text='randomania', variable=self.randomania).grid(row=1, column=0)
        tk.Checkbutton(self.args_frame, text='bapple', variable=self.bapple).grid(row=2, column=0)
        self.bentry = tk.Entry(self.args_frame, textvariable=bapple_nb, state=tk.DISABLED)
        self.bentry.grid(row=2, column=1)
        self.rentry = tk.Entry(self.args_frame, textvariable=self.rando, state=tk.DISABLED)
        self.rentry.grid(row=1, column=1)
        tk.Button(self.args_frame, text='print var',
                  command=lambda: print(convert_str_to_list(self.rando.get()))).grid(row=3, column=0)
        tk.Button(self.args_frame, text='open snake',
                  command=lambda: self.snakeuh(w)).grid(row=4, column=0)

        self.args_frame.grid(row=0, column=0)

        t1 = threading.Thread(target=self.loop)
        t1.start()

        ### pas du tout Ctrl + C  Ctrl + V
        self.color_frame = tk.Frame(w)

        self.color_var = tk.StringVar()
        self.color_var.set('modern')

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
    GuiTests()
