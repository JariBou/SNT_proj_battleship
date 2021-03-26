import tkinter as tk
from PIL import Image, ImageTk
from time import sleep, time

from src.resources.utils.Constants import Constants as Ct
path = Ct.get_path()
#button_load = Image.open(path.joinpath('resources\\images\\Chess\\taskbar.png'))


board = Ct.new_board()
for element in [thing for thing in board]:
    print(element)
