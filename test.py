import cv2
from tkinter import *
from PIL import Image, ImageTk
import io
import threading
import os
import sys


def resize(image):
    im = image
    new_siz = siz
    im.thumbnail(new_siz, Image.ANTIALIAS)
    return im


def size(event):
    global siz
    if siz == screenWH:
        siz = (600, 600)
    else:
        siz = screenWH
        win.state('zoomed')
    print('size is: ', siz)


def view_frame_video():
    vc = cv2.VideoCapture('con4.mp4')
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        img = Image.fromarray(frame)
        img = resize(img)
        imgtk = ImageTk.PhotoImage(img)
        lbl.config(image=imgtk)
        lbl.img = imgtk
        if stop:
            vc.release()
            break  # stop the loop thus stops updating the label and reading imagge frames
        cv2.waitKey(1)
    vc.release()


def stop_():
    global stop
    stop = True


def play():
    stop = False
    t = threading.Thread(target=view_frame_video)
    t.start()


root = Tk()
win = Toplevel()

stop = None
screenWH = (win.winfo_screenwidth(), win.winfo_screenheight())
siz = (800, 800)

Label(text='Press Play Button').pack()
frm_ = Frame(bg='black')
frm_.pack()
lbl = Label(frm_, bg='black')
lbl.pack(expand=True)
lbl.bind('<Double-Button-1>', size)

frm = Frame()
frm.pack()
Button(text='Play', command=play).pack(side=LEFT)
Button(text='Stop', command=stop_).pack(side=LEFT)

root.mainloop()


f = 1 + 1 + 1
g = 3 / 4
