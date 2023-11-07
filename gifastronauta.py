"""
from tkinter import *
import time
import os
root = Tk()

frameCnt = 12
frames = [PhotoImage(file='astronauta_flotando.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(151, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
"""
from tkinter import *
root = Tk()
myCanvas = Canvas(root)
myCanvas.pack()

def create_circle(x, y, r, canvas): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill="purple" )
create_circle(100, 100, 20, myCanvas)
create_circle(50, 25, 10, myCanvas)
root.mainloop()