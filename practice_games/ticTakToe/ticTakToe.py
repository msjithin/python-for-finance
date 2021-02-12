from tkinter import *
from tkinter import messagebox 
import random
import tkinter 
from PIL import ImageTk,Image  

root = Tk()
root.title('Tic Tak Toe')
root.resizable(width=False,height=False)
canv = Canvas(root, width=420, height=420, bd=0)
canv.pack() 
STEP = 115

reset = False
backkground = PhotoImage(file ="assets/background.png")
x_Photo = ImageTk.PhotoImage(Image.open("assets/x_2.png"))
o_Photo = ImageTk.PhotoImage(Image.open("assets/o_2.png"))
square_photo = ImageTk.PhotoImage(Image.open("assets/square.png"))

nClick = 0
x_clicked = [ 0 for i in range(9) ]
o_clicked = [ 0 for i in range(9) ]
x_Score , oScore = 0, 0
def reset_values():
    global nClick, x_clicked, o_clicked
    nClick = 0
    x_clicked = [ 0 for i in range(9) ]
    o_clicked = [ 0 for i in range(9) ]
    play()

canv.create_image(210,210, image=backkground)      
buttons = []
B00 = ''
B01 = ''
B02 = ''
B10 = ''
B11 = ''
B12 = '' 
B20 = ''
B21 = ''
B22 = ''
def player_x():
    pass

def player_o():
    pass
def check_score(clicks):
    if sum(clicks) > 2:
        for i in [0, 3, 6]:
            if clicks[i] + clicks[i+1] + clicks[i+2] == 3:
                return True
        for i in [0, 1, 2]:
            if clicks[i] + clicks[i+3] + clicks[i+6] == 3:
                return True
        if clicks[0] + clicks[4] + clicks[8] == 3:
            return True
        if clicks[2] + clicks[4] + clicks[6] == 3:
            return True
    return False

def buttonClicked(x, y, button):
    #print('clicked', y , x)
    global nClick, reset, x_Score, oScore
    nClick += 1
    if nClick % 2 == 0:
        button.configure(image = o_Photo)
        o_clicked[3*y + x] = 1
    else :
        button.configure(image = x_Photo)
        x_clicked[3*y + x] = 1
    if check_score(o_clicked):
        #print(' O won!')
        oScore += 1
        messagebox.showinfo("Score", " O won! \n X: {} \t O: {}".format(x_Score, oScore)) 
        reset_values()
    if check_score(x_clicked):
        #print(' X won!')
        x_Score += 1
        messagebox.showinfo("Score", " X won! \n X: {} \t O: {}".format(x_Score, oScore)) 
        reset_values()

class CanvasButton:
    def __init__(self, canvas, x, y):
        pivots = [ 58 , 210 , 350]
        self.canvas = canvas
        self.x = x
        self.y = y
        self.button = Button(canvas, image = square_photo,
                                command= lambda:buttonClicked(x , y, self.button))
        self.id = canvas.create_window(pivots[x], pivots[y], width=STEP, height=STEP,
                                       window=self.button)
        self.clicked = False
        self.player = -1
        


def play():
    B00 = CanvasButton(canv, 0, 0)
    B01 = CanvasButton(canv, 0, 1)
    B02 = CanvasButton(canv, 0, 2)
    B10 = CanvasButton(canv, 1, 0)
    B11 = CanvasButton(canv, 1, 1)
    B12 = CanvasButton(canv, 1, 2)
    B20 = CanvasButton(canv, 2, 0)
    B21 = CanvasButton(canv, 2, 1)
    B22 = CanvasButton(canv, 2, 2)

play()  
root.mainloop()
