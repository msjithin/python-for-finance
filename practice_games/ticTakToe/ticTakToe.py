from tkinter import *
import random 
from PIL import ImageTk,Image  

root = Tk()
root.title('Tic Tak Toe')
root.resizable(width=False,height=False)
canv = Canvas(root, width=420, height=420, bd=0)
canv.pack() 
STEP = 115
nClick = 0

def player_x():
    pass

def player_o():
    pass

backkground = PhotoImage(file ="assets/background.png")
#canv.create_image(0, 0, image=backkground)

# x_Photo = PhotoImage(file = "assets/x_2.png")
# o_Photo = PhotoImage(file = "assets/o_2.png")
x_Photo = ImageTk.PhotoImage(Image.open("assets/x_2.png"))
o_Photo = ImageTk.PhotoImage(Image.open("assets/o_2.png"))
square_photo = ImageTk.PhotoImage(Image.open("assets/square.png"))
xButton = Button(canv,image = x_Photo, command = player_x())
oButton = Button(canv,image = o_Photo, command = player_o())
squareButton = Button(canv,image = square_photo, command = player_o())

class CanvasButton:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.button = Button(canvas, image = square_photo,
                                command=self.buttonclicked)
        self.id = canvas.create_window(x, y, width=STEP, height=STEP,
                                       window=self.button)
        self.player = -1
    def buttonclicked(self):
        global nClick
        nClick += 1
        if nClick % 2 == 0:
            self.button.configure(image = x_Photo)
            self.player = 1
        else :
            self.button.configure(image = o_Photo)
            self.player = 0


canv.create_image(210,210, image=backkground)      
pivots = [ 58 , 210 , 350]
buttons = []
def play():
    for row in pivots:
        for column in pivots:
            buttons.append(CanvasButton(canv, row, column))
    


play()
root.mainloop()
