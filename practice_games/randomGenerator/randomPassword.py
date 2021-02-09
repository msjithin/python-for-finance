
import random
import string
import tkinter as tk


#create window
window = tk.Tk()
window.title('Random password generator')
window.geometry("400x400")
radioInput = tk.IntVar()

def get_random_string(length):
    #letters = string.ascii_lowercase  # only lowercase, alpha only
    #letters = string.ascii_letters    # lower and upper case, alpha only
    letters = string.ascii_letters + string.digits 
    if radioInput.get():
        letters +=  "()@!#%"
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print('for length', length, ' : ', result_str)
    return result_str

#functions
def phrase_generator():
    phrases = ["Hello", "What's up", "Aloha", "Ciao"]        
    name = str(entry1.get())
    return phrases[random.randint(0, 3)] +" "+name.capitalize()

def phrase_display():
    greeting = phrase_generator()
    #create text field
    greeting_display = tk.Text(master=window, height=1, width=30)
    greeting_display.grid(column=0, row=5)
    greeting_display.insert(tk.END, greeting)

def string_display():
    length = str(entry2.get())
    if not length.isnumeric():
        length = len(length)
    res = get_random_string(int(length)) 
    res_display = tk.Text(master=window, height=5, width=20)
    res_display.grid(column=0, row=16)
    res_display.insert(tk.END, res)




# label
title = tk.Label(text='Welcome to my app', font=("Times New Roman", 20))
title.grid(column=0, row=0)

label1 = tk.Label(text='Whats your name?')
label1.grid(column=0, row=3)
# entry field
entry1 = tk.Entry()
entry1.grid(column=1, row=3)
#button 1
button1 = tk.Button(text='Submit', bg="linen", command=phrase_display)
button1.grid(column=0, row=4)

subtitle = tk.Label(text='Lets generate randomized password')
subtitle.grid(column=0, row=6)
label2 = tk.Label(text='Length required')
label2.grid(column=0, row=8)

R1 = tk.Radiobutton(window, text="Alphanumeric", variable=radioInput, value=0)
R2 = tk.Radiobutton(window, text="Alphanumeric + charaters", variable=radioInput, value=1)
R1.grid()
R2.grid()
# entry field
entry2 = tk.Entry()
entry2.grid(column=1, row=8)
#button 2
button2 = tk.Button(text='Submit', bg="linen", command=string_display)
button2.grid(column=0, row=15)


window.mainloop()

