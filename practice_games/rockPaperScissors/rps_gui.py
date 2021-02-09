import random
import tkinter as tk
from tkinter.constants import ANCHOR, E, W 
from PIL import ImageTk,Image  

window = tk.Tk()
window.geometry("400x300")
window.title("Rock Paper Scissors Game") 

canv = tk.Canvas(window, width=80, height=80, bg='white')
leftPhoto = ImageTk.PhotoImage(Image.open("assets/rock.jpg"))
rightPhoto = ImageTk.PhotoImage(Image.open("assets/rock.jpg"))
canv.grid(row=1, column=2)
canv.create_image(10, 10, anchor=W, image=leftPhoto)
canv.create_image(10, 10, anchor=E, image=rightPhoto)

USER_SCORE = 0
COMP_SCORE = 0
USER_CHOICE = ""
COMP_CHOICE = ""
choice_map =  {0:'rock',1:'paper',2:'scissor'}

def choice_to_number(choice):
    for key in choice_map:
        if choice_map[key] == choice:
            return key

def number_to_choice(number):
    return choice_map[number]

def random_computer_choice():
    return random.choice(['rock','paper','scissor']) 

def show_text(answer):
    text_area = tk.Text(master=window,height=12,width=30,bg="#FFFF99")
    text_area.grid(column=0,row=4)
    text_area.insert(tk.END,answer)

def result(human_choice,comp_choice):
    global USER_SCORE
    global COMP_SCORE
    user=choice_to_number(human_choice)
    comp=choice_to_number(comp_choice)
    if(user==comp):
        print("Tie")
    elif((user-comp)%3==1):
        print("You win")
        USER_SCORE+=1
    else:
        print("Comp wins")
        COMP_SCORE+=1
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \n Your Score : {u} \n Computer Score : {c} ".format(uc=USER_CHOICE,cc=COMP_CHOICE,u=USER_SCORE,c=COMP_SCORE)    
    show_text(answer)

def rock():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='rock'
    COMP_CHOICE=random_computer_choice()
    result(USER_CHOICE,COMP_CHOICE)
def paper():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='paper'
    COMP_CHOICE=random_computer_choice()
    result(USER_CHOICE,COMP_CHOICE)
def scissor():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='scissor'
    COMP_CHOICE=random_computer_choice() 
    result(USER_CHOICE,COMP_CHOICE)

button1 = tk.Button(text="       Rock       ",bg="skyblue",command=rock)
button1.grid(column=0,row=1)
button2 = tk.Button(text="       Paper      ",bg="pink",command=paper)
button2.grid(column=0,row=2)
button3 = tk.Button(text="      Scissor     ",bg="lightgreen",command=scissor)
button3.grid(column=0,row=3)
show_text(' ')

window.mainloop()

