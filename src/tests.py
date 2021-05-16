from time import time
import tkinter as tk

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


def q():
    print('q')


def g():
    print('g')


if __name__ == '__main__':
    print(2//2)
    # w = tk.Tk('hello')
    # w.mainloop()

    lambda: q(), g()

    list_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(list_1[1:len(list_1)])
    kk = [-1]
    print(5 + kk[0])


#     list_1 = [a for a in range(100000)]
#     list_2 = [a for a in range(100000)]
#
#     start_for = time()
#     for k in list_1:
#         print(k)
#     for k in list_2:
#         print(k)
#     end_for = time()
#     difference_for = end_for - start_for
#
#     start_zip = time()
#     for k, i in enumerate(list_1):
#         print(k)
#         print(list_2[i])
#     end_zip = time()
#     difference_zip = end_zip - start_zip
#
#     print(f'''for loop: {difference_for}
# zip loop: {difference_zip}''')

