from tkinter import *
import pyautogui,os
from threading import Thread
import pytesseract
from googletrans import Translator
from PIL import Image,ImageTk
from pyperclip import copy
from glob import glob

#check if somebody didnt read the md file
windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
linux_path = r"/usr/share/tesseract-ocr/4.00/tessdata"
if os.name == "nt":
   if os.path.exists(windows_path):
      pytesseract.pytesseract.tesseract_cmd =windows_path
   else:
       tkinter.messagebox.showwarning("Exe not found","tesseract-ocr not found check github project page")
      
else:
   if os.path.exists(linux_path):
      pytesseract.pytesseract.tesseract_cmd =linux_path
   else:
         tkinter.messagebox.showwarning("Exe not found","tesseract-ocr not found check github project page (dude read the md file)")
        

translator = Translator()
destination_language = "tr"
def translate(sentence):
    return translator.translate(sentence,dest=destination_language)

#creating window
window=Tk()
window.title('Screen Translater')
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "pink")
window.config(bg='pink')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#uploading assets
def Loader(assetFolder):
    files = glob(f"{assetFolder}/*")
    paths = {};[paths.update({i.split("\\")[-1].split(".")[0]:i}) for i in files]
    def loadAsset(paths,name,size=None):
        if size: return ImageTk.PhotoImage(Image.open(paths[name]).resize(size))
        else: return ImageTk.PhotoImage(Image.open(paths[name]))
    return lambda name,size=None:loadAsset(paths,name,size)

loader = Loader("./images")
photo = loader("t",(22,22))
photo2 = loader("at",(20,20))
photo3 = loader("cursor",(35,30))
settingphoto = loader("settings",(30,30))
translatephoto = loader("translate",(35,35))

canvas = Canvas(window, bg="pink",width=screen_width-10, height=screen_height-10,highlightcolor="pink",highlightbackground="pink")
canvas.place(x=5,y=5)

running = False
clicked= False
rect = None
label = None
cursorAsset = None
starting=()
languages = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar', 'Japanese': 'ja', 'Azerbaijani': 'az', 'Kannada': 'kn', 'Basque': 'eu', 'Korean': 'ko', 'Bengali': 'bn', 'Latin': 'la', 'Belarusian': 'be', 'Latvian': 'lv', 'Bulgarian': 'bg', 'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk', 'Chinese Simplified': 'zh-CN', 'Malay': 'ms', 'Chinese Traditional': 'zh-TW', 'Maltese': 'mt', 'Croatian': 'hr', 'Norwegian': 'no', 'Czech': 'cs', 'Persian': 'fa', 'Danish': 'da', 'Polish': 'pl', 'Dutch': 'nl', 'Portuguese': 'pt', 'English': 'en', 'Romanian': 'ro', 'Esperanto': 'eo', 'Russian': 'ru', 'Estonian': 'et', 'Serbian': 'sr', 'Filipino': 'tl', 'Slovak': 'sk', 'Finnish': 'fi', 'Slovenian': 'sl', 'French': 'fr', 'Spanish': 'es', 'Galician': 'gl', 'Swahili': 'sw', 'Georgian': 'ka', 'Swedish': 'sv', 'German': 'de', 'Tamil': 'ta', 'Greek': 'el', 'Telugu': 'te', 'Gujarati': 'gu', 'Thai': 'th', 'Haitian Creole': 'ht', 'Turkish': 'tr', 'Hebrew': 'iw', 'Ukrainian': 'uk', 'Hindi':'hi', 'Urdu': 'ur', 'Hungarian': 'hu', 'Vietnamese': 'vi', 'Icelandic': 'is', 'Welsh': 'cy', 'Indonesian': 'id', 'Yiddish': 'yi'}
tkvar = StringVar(window)
options = [i for i in list(languages.keys())]

def move(widget:Canvas):
    def e(e):
      x,y=pyautogui.position()
      widget.place(x=x-(widget.winfo_width()/2),y=y-(widget.winfo_height()/2))
    widget.bind('<B1-Motion>',e)


def create(widget,x,y):
    widget.place(x=x,y=y)
    return widget

def defaultButtonFunctions(widget,buttonFunction):
    widget.bind("<Enter>",lambda x:widget.configure(bg="#84bbfc"))
    widget.bind("<Leave>",lambda x:widget.configure(bg="#2f84ea"))
    widget.bind("<Button-1>",lambda x:(widget.configure(bg="#7ab4fa"),buttonFunction(x)))

def translatePopup(text,translation):
    canvas = create(Canvas(window,width=180,height=120,bg="#2f84ea",highlightthickness=2, highlightbackground="gray"),150,70)
    move(canvas)
    closeButton = create(Label(canvas,text=" X ",bg="#2f84ea",fg="white"),158,4)
    iconButton = create(Label(canvas,image = photo,bg="#2f84ea"),8,2)
    copyButton = create(Label(canvas,image = photo2,bg="#2f84ea"),132,3)
    textbox = create(Text(canvas, height = 5, width = 20),9.5,30)
    textbox.insert(END,translation)
    defaultButtonFunctions(iconButton,lambda x:(os.startfile(f"https://translate.google.com/?sl=auto&tl={destination_language}&text={text}&op=translate")))
    defaultButtonFunctions(copyButton,lambda x:(copy(text)))
    defaultButtonFunctions(closeButton,lambda x:(canvas.destroy()))
    return canvas

box = None
def menuBar(cursor):
    canvas = create(Canvas(window,width=40,height=190,bg="#2f84ea",highlightthickness=2, highlightbackground="gray"),10,screen_height/2+50)
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Github",command=lambda :os.startfile("https://github.com/kaankarakoc42/translater"))
    def lang():
        global box
        x,y = pyautogui.position()
        tkvar.set(destination_language)
        def setLang(value):
            global destination_language,box
            destination_language = languages[value]
            box.destroy()
        box = create(OptionMenu(window,tkvar,*options,command=lambda x:setLang(x)),x+5,y)
        
    popup.add_command(label="language",command=lambda :lang())
    popup.add_separator()
    popup.add_command(label="Hide",command=lambda :(window.iconify()))
    def menu_popup(event):
        try: popup.tk_popup(event.x_root+50, event.y_root, 0)
        finally: popup.grab_release()
    settingsButton = create(Label(canvas,image = settingphoto,bg="#2f84ea"),5,10)
    defaultButtonFunctions(settingsButton,lambda x:(menu_popup(x)))
    translateButton = create(Label(canvas,image = translatephoto,bg="#2f84ea"),2,50)
    defaultButtonFunctions(translateButton,lambda x:(cursor()))
    closeButton = create(Label(canvas,text="Exit",bg="#2f84ea",fg="white"),10,160)
    defaultButtonFunctions(closeButton,lambda x:window.destroy())
    move(canvas)
    
#this motor functions are disgusting but I feel too lazy to change it :)
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
         widget.place(x=x-(wx/2)-5,y=y-(wy/2))
         if clicked:
            canvas.coords(rect,starting[0], starting[1], x-10,y-10)
            coord = (starting[0]+6,starting[1]+6,x-starting[0]-12,y-starting[1]-12)  


def doubleclick(widget,event):
    global running,clicked,starting,rect
    running = True
    clicked = True
    x,y=pyautogui.position()
    starting=(x-13,y-13)
    Thread(target = lambda :move_forward(widget,event)).start()
    if not rect:
        rect = canvas.create_rectangle(starting[0], starting[1],1,1, outline='red')

def cursorFunction():
    global cursorAsset
    x,y=pyautogui.position()
    if cursorAsset:
       cursorAsset.destroy()
    cursorAsset=create(Label(canvas,image = photo3,bg="pink",width=20,height=20),x+30,y-10)
    cursorAsset.bind("<Button-1>", lambda e:start_motor(cursorAsset,e))
    cursorAsset.bind("<ButtonRelease-1>", stop_motor)
    cursorAsset.bind("<Double-Button-1>",lambda e:doubleclick(cursorAsset,e))

menuBar(cursorFunction)                


window.mainloop()


