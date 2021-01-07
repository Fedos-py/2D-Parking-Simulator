from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import scrolledtext
from tkinter import *
import pygame
import os


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

def textbox():
    root = Tk()

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 300  # смещение от середины
    h = h - 300
    root.geometry('600x600+{}+{}'.format(w, h))
    #root.geometry('1000x700')
    root.resizable(False, False)

    '''text_box = Text(font=("Consolas", 18))
    text_box.pack(expand=Y, fill=BOTH)
    '''


    current_dir = os.path.dirname(os.path.abspath(__file__))
    file = open (f'{current_dir}/txt/prompt.txt', "r", encoding="utf-8")
    text = file.read()

    label = Label(text=text, font=("Consolas", 18), justify=LEFT)
    label.pack()
    root.update()

    '''
    text_box.insert("1.0", text)
    root.mainloop()
    '''


    #root.destroy()
