import ctypes
import threading
import tkinter as tk
from PIL.ImageTk import PhotoImage
from tkinter import font as ft, messagebox

from src import run_main
from src.resources.utils.Constants import Constants


#####          STATIC METHODS          ####
def g_help():
    messagebox.showinfo(title="Help & Rules",
                        message="Speed float is given as 1 over the number of squares it moves per second\n"
                                "(1 / 0.075 ~ 13.33squares/sec)")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 1.0")


####                                  ####


class Launcher:

    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Snake 2Players Launcher")
        menubar = tk.Menu(self.w)
        self.w.config(menu=menubar)
        self.w.resizable(width=False, height=False)
        self.create_menu(menubar)
        myappid = 'mjcorp.snake2p.alphav1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Constants.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\snake\\snake.ico'))

        self.bapple = tk.BooleanVar(value=False)
        self.speed = tk.DoubleVar(value=0.1)
        self.max_speed = tk.DoubleVar(value=0.01)
        self.bapple_nb = tk.IntVar(value=3)
        self.columns = tk.IntVar(value=50)
        self.lines = tk.IntVar(value=50)
        self.square_size = tk.IntVar(value=10)
        self.snake1_name = tk.StringVar(value="Random")
        self.snake2_name = tk.StringVar(value="Random")

        customFont = ft.Font(family='Source Sans Pro Black', size=17)
        self.running = True
        imgs = {'snake': PhotoImage(file=self.path.joinpath('resources\\images\\snake\\snake.png'))}
        tk.Label(self.w, borderwidth=10, relief="ridge", image=imgs['snake'], font=customFont).grid(row=0, column=1, sticky='n')

        self.args_frame = tk.Frame(self.w, borderwidth=6, relief="groove")
        tk.Label(self.args_frame, text='--Args--', font=customFont).grid(row=0, column=0, columnspan=2, sticky='n')
        tk.Checkbutton(self.args_frame, text='bapple', font=customFont, variable=self.bapple, anchor='w').grid(row=1,
                                                                                                               column=0,
                                                                                                               sticky='w')
        tk.Label(self.args_frame, text='Base speed(advanced)', font=customFont, anchor='w').grid(row=2, column=0,
                                                                                                 sticky='w')
        tk.Label(self.args_frame, text='Max speed(advanced)', font=customFont, anchor='w').grid(row=3, column=0,
                                                                                                sticky='w')
        self.bentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.bapple_nb, state=tk.DISABLED)
        self.bentry.grid(row=1, column=1)
        tk.Entry(self.args_frame, font=customFont, textvariable=self.speed).grid(row=2, column=1)
        tk.Entry(self.args_frame, font=customFont, textvariable=self.max_speed).grid(row=3, column=1)
        tk.Label(self.args_frame, text='Size:', font=customFont, anchor='w').grid(row=4, column=0, sticky='w')
        tk.Label(self.args_frame, text='columns: ', font=customFont, anchor='w').grid(row=5, column=0, sticky='w')
        tk.Entry(self.args_frame, textvariable=self.columns, font=customFont).grid(row=5, column=1)
        tk.Label(self.args_frame, text='lines: ', font=customFont, anchor='w').grid(row=6, column=0, sticky='w')
        tk.Entry(self.args_frame, textvariable=self.lines, font=customFont).grid(row=6, column=1)
        tk.Label(self.args_frame, text='square length: ', font=customFont, anchor='w').grid(row=7, column=0, sticky='w')
        tk.Entry(self.args_frame, textvariable=self.square_size, font=customFont).grid(row=7, column=1)
        tk.Label(self.args_frame, text='Snake 1 name: ', font=customFont, anchor='w').grid(row=8, column=0, sticky='w')
        tk.Entry(self.args_frame, textvariable=self.snake1_name, font=customFont).grid(row=8, column=1)
        tk.Label(self.args_frame, text='Snake 2 name: ', font=customFont, anchor='w').grid(row=9, column=0, sticky='w')
        tk.Entry(self.args_frame, textvariable=self.snake2_name, font=customFont).grid(row=9, column=1)
        self.args_frame.grid(row=0, column=0, rowspan=2)

        tk.Button(self.w, text='Open snake',
                  command=self.snakeuh, font=customFont, relief=tk.RAISED, border=10).grid(row=5, column=0, columnspan=2)

        self.t1 = threading.Thread(target=self.loop)
        self.t1.start()

        ### pas du tout Ctrl + C  Ctrl + V
        self.color_frame = tk.Frame(self.w, borderwidth=6, relief="solid")
        self.snake1_color = tk.StringVar()
        self.snake1_color.set('modern')
        tk.Label(self.color_frame, text='--Snake 1 Colors--', font=customFont).pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame, text='Modern', font=customFont, variable=self.snake1_color,
                                value='modern')
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame, text='Vintage', font=customFont, variable=self.snake1_color,
                                value='vintage')
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame, text='The Rock', font=customFont, variable=self.snake1_color,
                                value='therock')
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame, text='Dark Knight', font=customFont, variable=self.snake1_color,
                                value='darkknight')
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame, text='Outerworld', font=customFont,
                                variable=self.snake1_color, value='outerworld')
        radio5.pack(anchor='nw', padx=30)
        radio6 = tk.Radiobutton(self.color_frame, text='Ocean', font=customFont, variable=self.snake1_color,
                                value='ocean')
        radio6.pack(anchor='nw', padx=30)

        self.color_frame.grid(row=1, column=1)

        self.color_frame2 = tk.Frame(self.w, borderwidth=6, relief="solid")
        self.snake2_color = tk.StringVar()
        self.snake2_color.set('modern')
        tk.Label(self.color_frame2, text='--Snake 2 Colors--', font=customFont).pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame2, text='Modern', font=customFont, variable=self.snake2_color,
                                value='modern')
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame2, text='Vintage', font=customFont, variable=self.snake2_color,
                                value='vintage')
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame2, text='The Rock', font=customFont, variable=self.snake2_color,
                                value='therock')
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame2, text='Dark Knight', font=customFont, variable=self.snake2_color,
                                value='darkknight')
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame2, text='Outerworld', font=customFont,
                                variable=self.snake2_color, value='outerworld')
        radio5.pack(anchor='nw', padx=30)
        radio6 = tk.Radiobutton(self.color_frame2, text='Ocean', font=customFont, variable=self.snake2_color,
                                value='ocean')
        radio6.pack(anchor='nw', padx=30)

        self.color_frame2.grid(row=1, column=2)

        from src.resources.utils.Constants import Constants as Ct

        Ct.center(self.w)

        self.w.mainloop()

    def loop(self):
        while self.running:
            self.bentry.config(state=(tk.NORMAL if self.bapple.get() else tk.DISABLED))

    def snakeuh(self):
        from src.games.Snake.Snake2p import Game
        self.running = False
        self.w.destroy()
        Game(snake1_color=self.snake1_color.get(),
             snake2_color=self.snake2_color.get(),
             bapple=self.bapple.get(),
             nb_bapple=self.bapple_nb.get(),
             speed=self.speed.get(),
             nb_columns=self.columns.get(),
             nb_lines=self.lines.get(),
             square_dim=self.square_size.get(),

             snake1_name=self.snake1_name.get(),
             snake2_name=self.snake2_name.get(),

             max_speed=self.max_speed.get())

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=self.exit_launcher)

    def exit_launcher(self):
        self.running = False
        self.w.destroy()
        run_main.run_main()


if __name__ == '__main__':
    Launcher()
