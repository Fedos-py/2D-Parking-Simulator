from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *


def fileopen(**kwargs):
    root = Tk()
    root.withdraw()  # hide the window
    file = askopenfilename(**kwargs)
    root.destroy()
    return file

def filesave(**kwargs):
    root = Tk()
    root.withdraw()  # hide the window
    file = asksaveasfilename(**kwargs)
    root.destroy()
    return file