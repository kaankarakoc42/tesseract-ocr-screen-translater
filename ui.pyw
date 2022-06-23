from tkinter import *
import pyautogui,os
from threading import Thread
import pytesseract
from googletrans import Translator
from PIL import Image,ImageTk
from pyperclip import copy

translator = Translator()

def translate(sentence):
    return translator.translate(sentence,dest="tr")

pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"


window=Tk()
window.title('Screen Translater')
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "pink")
window.config(bg='pink')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

img= Image.open('t.png').resize((22,22))
photo = ImageTk.PhotoImage(img)
img2= Image.open('at.png').resize((20,20))
photo2 = ImageTk.PhotoImage(img2)

canvas = Canvas(window, bg="pink",width=screen_width-10, height=screen_height-10)
canvas.place(x=5,y=5)

running = False
clicked= False
rect = None
label = None
starting=()

def move(widget):
    def e(e):
      x,y=pyautogui.position()
      widget.place(x=x-100,y=y-10)
    widget.bind('<B1-Motion>',e)

def translatePopup(text,translation):
    canvas = Canvas(window,width=180,height=120,bg="#2f84ea",highlightthickness=2, highlightbackground="gray")
    move(canvas)
    canvas.place(x=150,y=70)
    closeButton = Label(canvas,text=" X ",bg="#2f84ea",fg="white")
    closeButton.place(x=158,y=4)
    iconButton = Label(canvas,image = photo,bg="#2f84ea")
    iconButton.place(x=7,y=2)
    iconButton.bind("<Enter>",lambda x:iconButton.configure(bg="lightblue"))
    iconButton.bind("<Leave>",lambda x:iconButton.configure(bg="#2f84ea"))
    iconButton.bind("<Button-1>",lambda x:(iconButton.configure(bg="#D8EFED"),os.startfile(f"https://translate.google.com/?sl=auto&tl=tr&text={text}&op=translate")))
    copyButton = Label(canvas,image = photo2,bg="#2f84ea")
    copyButton.place(x=132,y=3)
    textbox = Text(canvas, height = 5, width = 20)
    textbox.place(x=9.5,y=30)
    textbox.insert(END,translation)
    copyButton.bind("<Enter>",lambda x:copyButton.configure(bg="lightblue"))
    copyButton.bind("<Leave>",lambda x:copyButton.configure(bg="#2f84ea"))
    copyButton.bind("<Button-1>",lambda x:(copyButton.configure(bg="#D8EFED"),copy(text)))
    closeButton.bind("<Enter>",lambda x:closeButton.configure(bg="lightblue"))
    closeButton.bind("<Leave>",lambda x:closeButton.configure(bg="#2f84ea"))
    closeButton.bind("<Button-1>",lambda x:(closeButton.configure(bg="#D8EFED"),canvas.destroy()))
    return canvas
def start_motor(widget,event):
    global running
    running = True
    Thread(target = lambda :move_forward(widget,event)).start()

def stop_motor(event):
    global running,clicked,label
    running = False
    if clicked:
       text =pytesseract.image_to_string(pyautogui.screenshot(region=coord))
       textTranslation =translate(text).text
       label=translatePopup(text,textTranslation)
       clicked = False
       canvas.coords(rect,0, 0,0,0)

def move_forward(widget:Canvas,event):
    global coord,label
    if label:
       label.destroy()
    while running:
         x,y=pyautogui.position()
         wx,wy=widget.winfo_width(),widget.winfo_height()
         widget.place(x=x-10,y=y-10)
         if clicked:
            canvas.coords(rect,starting[0], starting[1], x-10,y-10)
            coord = (starting[0]+6,starting[1]+6,x-starting[0]-12,y-starting[1]-12)  
         i=0
         while i<=1000:
               i+=1

def doubleclick(widget,event):
    global running,clicked,starting,rect
    running = True
    clicked = True
    x,y=pyautogui.position()
    starting=(x-10,y-10)
    Thread(target = lambda :move_forward(widget,event)).start()
    if not rect:
        rect = canvas.create_rectangle(starting[0], starting[1],1,1, outline='red')

                 
mainCanvas=Canvas(canvas, bg="grey", height=15, width=15)

mainCanvas.place(x=0,y=0)
mainCanvas.bind("<Button-1>", lambda e:start_motor(mainCanvas,e))
mainCanvas.bind("<ButtonRelease-1>", stop_motor)
mainCanvas.bind("<Double-Button-1>",lambda e:doubleclick(mainCanvas,e))

window.mainloop()

