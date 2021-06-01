from tkinter import *
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import textwrap
import pyttsx3
import pandas as pd
import numpy as np
import re
import os

print(os. getcwd())
data = pd.read_csv('./data_cleaning/output.csv')

word_search = "Word"
word_mean = "Definition of word"
word_example ="Show a example of your word"

#Form code
root = Tk()
def speaker_word():
	engine = pyttsx3.init()
	engine.say(my_input.get())
	engine.runAndWait()
def speaker_sen():
	x = my_input.get()
	y = data.loc[lambda data: data['paragraph_arr'] == x.upper(),["sentence"][0]].iloc[0]
	engine = pyttsx3.init()
	engine.say(y)
	engine.runAndWait()

def add_meaning():
    df = pd.DataFrame(
        {
            'paragraph_arr': my_input.get(),
            'freq': 1000,
            'title': 100,
            'rank': 3000,
            'meaning': my_mean.get(),
            'example': my_input.get(),
            'sentence': my_input.get(),
            'rating': 4
        }, index=[0]
    )
    with open('./data_cleaning/output.csv', 'a') as f:
        df.to_csv(f, mode='a', header=False, index=False)

my_mean = tk.StringVar()
def addmeaning():
	sub_form = Toplevel(root)
	sub_form.geometry("400x250")
	sub_form.title("Add new word's meaning!")

	lb_subword=Label(sub_form, text= "New word: ", fg='black', font=("Helvetica", 13,))
	lb_subword.place(x=10, y=35)
	lb_subword=Label(sub_form, text= my_input.get().upper(), fg='red', font=("Helvetica", 13,'bold'))
	lb_subword.place(x=100, y=35)
	lb_submean=Label(sub_form, text= "Difinition: ", fg='blue', font=("Helvetica", 13,))
	lb_submean.place(x=10, y=65)
	lb_done = Label(sub_form, text= "  ", fg='red', font=("Helvetica", 13,)).place(x=100, y=200)

	btnadd = Button(sub_form, text = '   Add   ', bd = '5',command = add_meaning)
	btnadd.place(x = 330, y = 105)

	btnsub = Button(sub_form, text = '   OK!   ', bd = '5',command = sub_form.destroy)
	btnsub.place(x = 330, y = 200)

	#my_mean = tk.StringVar()
	input_mean = ttk.Entry(sub_form, width = 30,font=('helvetica', 13, 'italic'), textvariable = my_mean )
	input_mean.place(x=10, y=105)

	#btn_subadd = Button(sub_form, text = "OK",fg='red', font=("Helvetica", 10,'bold'))
	#btnsub = canvas.create_window(300, 200, anchor="nw", window = btn_subadd)
	sub_form.resizable(0, 0)
	sub_form.mainloop()
root.title('Data Science - Dictionary')
root.geometry("600x400")
	#root.iconbitmap("D:/02.Project/Edu/Dic/icon.ico")
	#root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='D:/02.Project/Edu/Dic/icon.png'))

bg= ImageTk.PhotoImage(file='./interface/background.png')
canvas = Canvas(root,width=600, height = 400)
canvas.pack(expand=True, fill = BOTH)
canvas.create_image(0,0,image = bg, anchor = "nw")

my_form = Frame(root)
my_form.pack(pady=5)

my_menu = Menu(root)
root.config(menu = my_menu)

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label ="Dictionary",menu=file_menu)
file_menu.add_command(label="Eng - Vie")
file_menu.add_command(label="Vie - Eng")
file_menu.add_separator()
file_menu.add_command(label="China - Vie")
file_menu.add_command(label="Viet - China")
file_menu.add_separator()
file_menu.add_command(label="Exit", command = root.destroy)

edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label ="Information",menu=edit_menu)
edit_menu.add_command(label="Arthur")
edit_menu.add_command(label="Lisence")
edit_menu.add_command(label="Reference")
edit_menu.add_command(label="Webside")

Help_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label ="Help",menu=Help_menu)
Help_menu.add_command(label="Feed back!")
Help_menu.add_command(label="Contact")
Help_menu.add_command(label="Help")

canvas.create_text(50,35,text="Eng - Vie",font=('helvetica', 15, 'bold'))

#textbox input word
my_input = tk.StringVar()
input_Entered = ttk.Entry(root, width = 30,font=('helvetica', 15, 'italic'), textvariable = my_input )
input_Entered.place(x=120, y=20)

def getTextInput():
    word_search = my_input.get()
    word_search = word_search.upper()
    if word_search not in data['paragraph_arr'].unique():
    	#print('False')
    	lb_mean.config(text = 'Not found this word in database. You can add into database!')
    	lb_example.config(text = ' ')
    	Label(root, text= 'Popular rating:   0/4', fg='red', font=("Helvetica", 11)).place(x=10, y=370)
    if word_search in data['paragraph_arr'].unique():
	    Label(root, text= "["+word_search+']                          ', fg='red', font=("Helvetica", 15, 'bold')).place(x=10, y=65)
	    my_wrap = textwrap.TextWrapper(width = 60)
	    word_mean = data.loc[lambda data: data['paragraph_arr'] == word_search,["meaning"][0]].iloc[0]
	    lb_mean.config(text = format(my_wrap.fill(text = word_mean)))
	    word_example = data.loc[lambda data: data['paragraph_arr'] == word_search,["sentence"][0]].iloc[0]
	    lb_example.config(text = format(my_wrap.fill(text = word_example)))
	    Label(root, text= 'Popular rating:   '+ str(data.loc[lambda data: data['paragraph_arr'] == word_search,["rating"][0]].iloc[0])+'/4', fg='red', font=("Helvetica", 11)).place(x=10, y=370)
image_search = PhotoImage(file = "./interface/search.png")
btn_search = Button(root, image = image_search,command = getTextInput)
btn1 = canvas.create_window(500, 18, anchor="nw", window = btn_search)
#_____
btn_add = Button(root, text = "Add meaning",fg='red', font=("Helvetica", 10,'bold'),command=addmeaning)
btn2 = canvas.create_window(480, 350, anchor="nw", window = btn_add)

image_speaker = PhotoImage(file = "./interface/speaker.png")
btn_speakword = Button(root, image = image_speaker, command = speaker_word)
btn3 = canvas.create_window(480, 65, anchor="nw", window = btn_speakword)

#btn4 = canvas.create_window(480, 225, anchor="nw", window = btn_speaksen)
#output
#lb_word=Label(root, text= "["+word_search+']', fg='red', font=("Helvetica", 15, 'bold'))
#lb_word.place(x=10, y=65)

lb_dinhnghia=Label(root, text="* Definition:", fg='blue', font=("Helvetica", 13))
lb_dinhnghia.place(x=10, y=100)

lb_mean=Label(root, text= word_mean, fg='black', font=("Helvetica", 11),anchor = "w",justify=LEFT)
lb_mean.place(x=50, y=125)

lb_vidu=Label(root, text="* Example:", fg='blue', font=("Helvetica", 13))
lb_vidu.place(x=10, y=200)

my_wrap = textwrap.TextWrapper(width = 60)
#word_example =format(my_wrap.fill(text = word_example))

lb_example = Label(root, text = format(my_wrap.fill(text = word_example)), fg='black', font=("Helvetica", 11),anchor = "w",justify=LEFT)
lb_example.place(x=50, y=225)

status_bar = Label(root,text="Ready   ", anchor=E)
status_bar.pack(fill=X,side= BOTTOM, ipady = 5)
root.resizable(0,0)
root.mainloop()
