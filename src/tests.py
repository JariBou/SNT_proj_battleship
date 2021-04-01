import tkinter as tk
from PIL import Image, ImageTk
from time import sleep, time

from src.resources.utils.Constants import Constants as Ct
path = Ct.get_path()
#button_load = Image.open(path.joinpath('resources\\images\\Chess\\taskbar.png'))


class A:

    def a(self):
        return 'a'


class B:

    def a(self):
        return 'b'


class C(A, B):

    def total(self):
        string = A.a(self)
        string += B.a(self)
        return string


if __name__ == '__main__':
    C = C()
    print([None] * 7)
