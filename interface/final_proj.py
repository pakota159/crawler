import os
import sys
import threading

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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# External files
output_file = resource_path('data_cleaning/output.csv')
background_img = resource_path('interface/background.png')
search_img = resource_path('interface/search.png')
speaker_img = resource_path('interface/speaker.png')

# Raw data
data = pd.read_csv(output_file)
word_search = "Word"
word_mean = "Definition of word"
word_example ="Show a example of your word"

# Form code
root = Tk()

root.title('Data Science - Dictionary')
root.geometry("600x400")

# Background
bg= ImageTk.PhotoImage(file=background_img)
canvas = Canvas(root,width=600, height = 400)
canvas.pack(expand=True, fill = BOTH)
canvas.create_image(0,0,image = bg, anchor = "nw")

canvas.create_text(50,35,text="Eng - Vie",font=('helvetica', 15, 'bold'))

# textbox input word
my_input = tk.StringVar()
input_Entered = ttk.Entry(root, width = 30,font=('helvetica', 15, 'italic'), textvariable = my_input )
input_Entered.place(x=120, y=20)

def speaker_word(input_text):
	engine = pyttsx3.init()
	engine.say(input_text)
	engine.runAndWait()

def speaker_sen():
	sentence = data.loc[lambda data: data['paragraph_arr'] == my_input.get().upper(),["sentence"][0]].iloc[0]
	speaker_word(sentence)
	
def add_meaning_to_file():
	df = pd.DataFrame(
		{
			'paragraph_arr': my_input.get(),
			'freq': 1000,
			'title': 100,
			'rank': 3000,
			'meaning': my_mean.get(),
			'example': my_input.get(),
			'sentence': my_input.get(),
			'rating': 1
		}, index=[0]
	)

	data.loc[data.index.max() + 1] = [my_input.get(), 1000, 100, 3000, my_mean.get(), my_input.get(), my_input.get(), 1]
	with open(output_file, 'a') as f:
		df.to_csv(f, mode='a', header=False, index=False)
		
my_mean = tk.StringVar()

def add_meaning():
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

	btnadd = Button(sub_form, text = '   Add   ', bd = '5',command = add_meaning_to_file)
	btnadd.place(x = 330, y = 105)

	btnsub = Button(sub_form, text = '   OK!   ', bd = '5',command = sub_form.destroy)
	btnsub.place(x = 330, y = 200)

	input_mean = ttk.Entry(sub_form, width = 30,font=('helvetica', 13, 'italic'), textvariable = my_mean )
	input_mean.place(x=10, y=105)

	sub_form.resizable(0, 0)
	sub_form.mainloop()



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
	    rating = ''
	    if str(data.loc[lambda data: data['paragraph_arr'] == word_search,["rating"][0]].iloc[0]) == '1':
	    	rating = "Very Important"
	    elif str(data.loc[lambda data: data['paragraph_arr'] == word_search,["rating"][0]].iloc[0]) == '2':
	    	rating ='Important'
	    elif str(data.loc[lambda data: data['paragraph_arr'] == word_search,["rating"][0]].iloc[0]) == '3':
	    	rating = 'Normal'
	    else :
	    	rating = 'Rare'
	    Label(root, text= 'Popular rating:   '+ rating, fg='red', font=("Helvetica", 11)).place(x=10, y=370)

# Search button
image_search = PhotoImage(file = search_img)
btn_search = Button(root, image = image_search,command = getTextInput)
canvas.create_window(500, 18, anchor="nw", window = btn_search)

# Add meaning button
btn_add = Button(root, text = "Add meaning",fg='red', font=("Helvetica", 10,'bold'),command=add_meaning)
canvas.create_window(480, 350, anchor="nw", window = btn_add)

# Speaker button
image_speaker = PhotoImage(file = speaker_img)
btn_speakword = Button(root, image = image_speaker, command = lambda: threading.Thread(target=speaker_word, daemon=True).start())
canvas.create_window(480, 65, anchor="nw", window = btn_speakword)

lb_dinhnghia=Label(root, text="* Definition:", fg='blue', font=("Helvetica", 13))
lb_dinhnghia.place(x=10, y=100)

lb_mean=Label(root, text= word_mean, fg='black', font=("Helvetica", 11),anchor = "w",justify=LEFT)
lb_mean.place(x=50, y=125)

lb_vidu=Label(root, text="* Example:", fg='blue', font=("Helvetica", 13))
lb_vidu.place(x=10, y=200)

my_wrap = textwrap.TextWrapper(width = 60)

lb_example = Label(root, text = format(my_wrap.fill(text = word_example)), fg='black', font=("Helvetica", 11),anchor = "w",justify=LEFT)
lb_example.place(x=50, y=225)

status_bar = Label(root,text="Ready   ", anchor=E)
status_bar.pack(fill=X,side= BOTTOM, ipady = 5)

root.resizable(0,0)
root.mainloop()
