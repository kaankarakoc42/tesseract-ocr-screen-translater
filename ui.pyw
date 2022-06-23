from tkinter import *
import pyautogui
from threading import Thread
import pytesseract
from googletrans import Translator
translator = Translator()
from PIL import Image,ImageTk

def translate(sentence):
    return translator.translate(sentence,dest="tr")

pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"
window=Tk()
img= ImageTk.PhotoImage(Image.open("b .png"))
# add widgets here
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", True)
#window.wm_attributes("-disabled", True)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
mid = (screen_height,screen_width)
window.wm_attributes("-transparentcolor", "white")
window.config(bg='white')
window.geometry("300x200+10+20")
coord = ()
frame1 = Frame(window, width=screen_width, height=screen_height,bg="grey",highlightbackground="black", borderwidth=1)
frame1.place(x=0,y=0)
#frame2 = Frame(window, width=screen_width-10, height=screen_height-10,bg="white",highlightbackground="black", borderwidth=1)
canvas = Canvas(window, bg="white",width=screen_width-10, height=screen_height-10)
canvas.place(x=5,y=5)
running = False
clicked= False
rect = None
label = None
starting=()
def start_motor(widget,event):
    global running
    print("starting motor...")
    running = True
    t = Thread(target = lambda :move_forward(widget,event))
    t.start()

def stop_motor(event):
    global running,clicked,label
    running = False
    print("stopping motor...")
    if clicked:
       text =translate(pytesseract.image_to_string(pyautogui.screenshot(region=coord))).text
       label = Label(canvas, text = text)
       label.place(x=100,y=100)
       clicked = False
       canvas.coords(rect,0, 0,0,0)

def move_forward(widget:Canvas,event):
    global coord,label
    if label:
       label.destroy()
    while running: # Thread will run infinitely in the background
         x,y=pyautogui.position()
         #print(x,y,event.x,event.y)
         wx,wy=widget.winfo_width(),widget.winfo_height()
         #widget.place(x=x-event.x,y=y-event.y)
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
    
    print("double")
    t = Thread(target = lambda :move_forward(widget,event))
    t.start()
    if not rect:
        rect = canvas.create_rectangle(starting[0], starting[1],1,1, outline='red')

                 
mainCanvas=Canvas(canvas, bg="grey", height=15, width=15)
#mainCanvas.create_image(0,0,anchor =NW,image=img)
mainCanvas.place(x=0,y=0)
mainCanvas.bind("<Button-1>", lambda e:start_motor(mainCanvas,e))
mainCanvas.bind("<ButtonRelease-1>", stop_motor)
mainCanvas.bind("<Double-Button-1>",lambda e:doubleclick(mainCanvas,e))


window.title('Hello Python')
window.mainloop()
