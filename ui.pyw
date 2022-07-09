from tkinter import *
from tkinter import messagebox
import pyautogui,os,pytesseract
from googletrans import Translator
from PIL import Image,ImageTk
from pyperclip import copy
from glob import glob

        

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

#check if somebody didnt read the md file
windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
linux_path = r"/usr/share/tesseract-ocr/4.00/tessdata"
if os.name == "nt":
   if os.path.exists(windows_path):
      pytesseract.pytesseract.tesseract_cmd =windows_path
   else:
       messagebox.showwarning("Exe not found","tesseract-ocr not found check github project page")
      
else:
   if os.path.exists(linux_path):
      pytesseract.pytesseract.tesseract_cmd =linux_path
   else:
         messagebox.showwarning("Exe not found","tesseract-ocr not found check github project page (dude read the md file)")
         
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

languages = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar', 'Japanese': 'ja', 'Azerbaijani': 'az', 'Kannada': 'kn', 'Basque': 'eu', 'Korean': 'ko', 'Bengali': 'bn', 'Latin': 'la', 'Belarusian': 'be', 'Latvian': 'lv', 'Bulgarian': 'bg', 'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk', 'Chinese Simplified': 'zh-CN', 'Malay': 'ms', 'Chinese Traditional': 'zh-TW', 'Maltese': 'mt', 'Croatian': 'hr', 'Norwegian': 'no', 'Czech': 'cs', 'Persian': 'fa', 'Danish': 'da', 'Polish': 'pl', 'Dutch': 'nl', 'Portuguese': 'pt', 'English': 'en', 'Romanian': 'ro', 'Esperanto': 'eo', 'Russian': 'ru', 'Estonian': 'et', 'Serbian': 'sr', 'Filipino': 'tl', 'Slovak': 'sk', 'Finnish': 'fi', 'Slovenian': 'sl', 'French': 'fr', 'Spanish': 'es', 'Galician': 'gl', 'Swahili': 'sw', 'Georgian': 'ka', 'Swedish': 'sv', 'German': 'de', 'Tamil': 'ta', 'Greek': 'el', 'Telugu': 'te', 'Gujarati': 'gu', 'Thai': 'th', 'Haitian Creole': 'ht', 'Turkish': 'tr', 'Hebrew': 'iw', 'Ukrainian': 'uk', 'Hindi':'hi', 'Urdu': 'ur', 'Hungarian': 'hu', 'Vietnamese': 'vi', 'Icelandic': 'is', 'Welsh': 'cy', 'Indonesian': 'id', 'Yiddish': 'yi'}
tkvar = StringVar(window)
options = [i for i in list(languages.keys())]
rect = None
startingPoint = ()
rectDrawingState = False
realesedButtons=0
coords = ()

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
def menuBar():
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
    defaultButtonFunctions(translateButton,lambda x:(grabScreen()))
    closeButton = create(Label(canvas,text="Exit",bg="#2f84ea",fg="white"),10,160)
    defaultButtonFunctions(closeButton,lambda x:window.destroy())
    move(canvas)

    
def setStarting(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    startingPoint = pyautogui.position()
    rectDrawingState = True
    if not rect:
       rect = canvas.create_rectangle(startingPoint[0], startingPoint[1],2,2, outline='red')

def setEnding(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    if not rectDrawingState: return
    x,y=pyautogui.position()
    canvas.coords(rect,startingPoint[0], startingPoint[1], x,y)
    coords = [int(i) for i in (startingPoint[0]+1,startingPoint[1]+1,x-startingPoint[0]-1,y-startingPoint[1]-1)]
    
def drawingDone(canvas):
    global rectDrawingState,rect,coords;
    rectDrawingState = False
    canvas.delete(rect)
    canvas.destroy()
    rect = None

def on_double_click_release(func):
    global realesedButtons;
    if not rectDrawingState: return
    if realesedButtons >= 1:
       func()
       realesedButtons = 0
    realesedButtons+=1

def on_release(canvas):
    global realesedButtons;
    drawingDone(canvas)
    window.attributes('-alpha', 1)
    window.config(cursor="arrow")
    window.update()
    realesedButtons = 0
    #print(coords,pyautogui.screenshot(region=coords).show())
    text =pytesseract.image_to_string(pyautogui.screenshot(region=coords))
    textTranslation = translate(text).text
    translatePopup(text,textTranslation)

    
def grabScreen():
    canvas = create(Canvas(window,width = screen_width,height=screen_height),0,0)
    window.config(cursor="tcross")
    window.attributes('-alpha', 0.3)
    canvas.bind("<Double-Button-1>",lambda x:setStarting(canvas))
    canvas.bind("<B1-Motion>",lambda x:setEnding(canvas))
    canvas.bind("<ButtonRelease-1>",lambda x:on_double_click_release(lambda :on_release(canvas)))


menuBar()                
window.mainloop()

