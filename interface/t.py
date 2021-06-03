import pyttsx3
import threading
from tkinter import *

def speaker_word():
    engine = pyttsx3.init()
    engine.say("Get absolute path to resource")
    engine.runAndWait()

root = Tk()
root.title('Data Science - Dictionary')
root.geometry("600x400")

canvas = Canvas(root,width=600, height = 400)
canvas.pack(expand=True, fill = BOTH)

my_form = Frame(root)
my_form.pack(pady=5)

canvas.create_text(50,35,text="Eng - Vie",font=('helvetica', 15, 'bold'))

btn_speakword = Button(root, text = "BUTTON", command = lambda: threading.Thread(target=speaker_word, daemon=True).start())
canvas.create_window(480, 65, anchor="nw", window = btn_speakword)

root.resizable(0,0)
root.mainloop()
