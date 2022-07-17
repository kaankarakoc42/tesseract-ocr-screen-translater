from tkinter import *
from tkinter import messagebox
from googletrans import Translator
from PIL import Image,ImageTk,ImageGrab
from pyperclip import copy
from glob import glob
from threading import Thread
from subprocess import run
import ctypes
import ctypes.wintypes
from time import time
import os

def timer(function):
    def wrapper(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        end = time()
        print(f'[{function.__name__}] It took {(end-start):.3f} seconds')

    return wrapper

def position():
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return cursor.x,cursor.y

def screenshot(imageFilename=None, region=None):
    im = ImageGrab.grab()
    if region is not None:
        assert len(region) == 4, 'region argument must be a tuple of four ints'
        region = [int(x) for x in region]
        im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))
    return im

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

if os.name == "nt":
   if os.path.exists(windows_path):
      tesseract_path = windows_path
   else:
       messagebox.showwarning("Exe not found","tesseract-ocr not found check github project page")
else:
    exit()
      
def image_to_string(image:Image):
    image.save("./te.png")
    x=run(f'"{tesseract_path}" ./te.png  - pm20', capture_output=True, text=True,shell=True).stdout.lower()
    os.remove("./te.png")
    print(x)
    return x

#colors 
blue="#2f84ea"
dark = "#1c1d22"
dbfe = "#84bbfc"
dbfb = "#7ab4fa"
theme = blue

#uploading assets
folder_path = os.path.abspath(os.getcwd()) 
def replaceColor(picture,datas=None):
    if datas==None: return picture
    oldHex,newHex=datas
    width, height = picture.size
    print(width,height)
    hexToRgb =lambda hex:tuple(int(hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    for x in range(width):
        for y in range(height):
            current_color = picture.getpixel( (x,y) )
            if current_color == hexToRgb(oldHex):
                picture.putpixel( (x,y), hexToRgb(newHex))
    return picture

def Loader(assetFolder):
    files = glob(f"{assetFolder}/*")
    paths = {};[paths.update({i.split("\\")[-1].split(".")[0]:i}) for i in files]
    def loadAsset(paths,name,size=None,replaceColorHex=None):
        if size: 
           #replaceColor(Image.open(paths[name]),datas=replaceColorHex).resize(size).save(f"./images/dark/{name}.png")
           return ImageTk.PhotoImage(replaceColor(Image.open(paths[name]),datas=replaceColorHex).resize(size))
        else: return ImageTk.PhotoImage(replaceColor(Image.open(paths[name]),datas=replaceColorHex))
    return lambda name,size=None,replaceColorHex=None:loadAsset(paths,name,size,replaceColorHex)

@timer
def setTheme(stheme):
    if stheme == "dark":
        theme = dark
        dbfe = "#373943"
        dbfb = "#5d6171"
        loader = Loader(f"{folder_path}/images/dark")
    elif stheme == "blue":
        loader = Loader(f"{folder_path}/images/blue")
    photo = loader("translateIcon",(22,22))
    photo2 = loader("clipboardIcon",(22,22))
    settingphoto = loader("settingsIcon",(35,35))
    translatephoto = loader("translateMenuIcon",(35,35))
    globals().update(locals())



languages = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar', 'Japanese': 'ja', 'Azerbaijani': 'az', 'Kannada': 'kn', 'Basque': 'eu', 'Korean': 'ko', 'Bengali': 'bn', 'Latin': 'la', 'Belarusian': 'be', 'Latvian': 'lv', 'Bulgarian': 'bg', 'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk', 'Chinese Simplified': 'zh-CN', 'Malay': 'ms', 'Chinese Traditional': 'zh-TW', 'Maltese': 'mt', 'Croatian': 'hr', 'Norwegian': 'no', 'Czech': 'cs', 'Persian': 'fa', 'Danish': 'da', 'Polish': 'pl', 'Dutch': 'nl', 'Portuguese': 'pt', 'English': 'en', 'Romanian': 'ro', 'Esperanto': 'eo', 'Russian': 'ru', 'Estonian': 'et', 'Serbian': 'sr', 'Filipino': 'tl', 'Slovak': 'sk', 'Finnish': 'fi', 'Slovenian': 'sl', 'French': 'fr', 'Spanish': 'es', 'Galician': 'gl', 'Swahili': 'sw', 'Georgian': 'ka', 'Swedish': 'sv', 'German': 'de', 'Tamil': 'ta', 'Greek': 'el', 'Telugu': 'te', 'Gujarati': 'gu', 'Thai': 'th', 'Haitian Creole': 'ht', 'Turkish': 'tr', 'Hebrew': 'iw', 'Ukrainian': 'uk', 'Hindi':'hi', 'Urdu': 'ur', 'Hungarian': 'hu', 'Vietnamese': 'vi', 'Icelandic': 'is', 'Welsh': 'cy', 'Indonesian': 'id', 'Yiddish': 'yi'}
tkvar = StringVar(window)
options = [i for i in list(languages.keys())]
rect = None
startingPoint = ()
rectDrawingState = False
coords = ()
box = None

def move(widget:Canvas):
    def e(e):
      x,y=position()
      widget.place(x=x-(widget.winfo_width()/2),y=y-(widget.winfo_height()/2))
    widget.bind('<B1-Motion>',e)


def create(widget,x,y):
    widget.place(x=x,y=y)
    return widget

def defaultButtonFunctions(widget,buttonFunction):
    widget.bind("<Enter>",lambda x:widget.configure(bg=dbfe))
    widget.bind("<Leave>",lambda x:widget.configure(bg=theme))
    widget.bind("<Button-1>",lambda x:(widget.configure(bg=dbfb),buttonFunction(x)))

@timer
def translatePopup(text,translation):
    canvas = create(Canvas(window,width=180,height=120,bg=theme,highlightthickness=2, highlightbackground="gray"),150,70)
    move(canvas)
    closeButton = create(Label(canvas,text=" X ",bg=theme,fg="white"),158,4)
    iconButton = create(Label(canvas,image = photo,bg=theme),8,2)
    copyButton = create(Label(canvas,image = photo2,bg=theme),132,3)
    textbox = create(Text(canvas, height = 5, width = 20),9.5,30)
    textbox.insert(END,translation)
    defaultButtonFunctions(iconButton,lambda x:(os.startfile(f"https://translate.google.com/?sl=auto&tl={destination_language}&text={text}&op=translate")))
    defaultButtonFunctions(copyButton,lambda x:(copy(text)))
    defaultButtonFunctions(closeButton,lambda x:(canvas.destroy()))
    return canvas

@timer
def menuBar():
    canvas = create(Canvas(window,width=40,height=190,bg=theme,highlightthickness=2, highlightbackground="gray"),10,screen_height/2+50)
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Github",command=lambda :os.startfile("https://github.com/kaankarakoc42/translater"))
    def lang():
        global box
        x,y = position()
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
    settingsButton = create(Label(canvas,image = settingphoto,bg=theme),2,10)
    defaultButtonFunctions(settingsButton,lambda x:(menu_popup(x)))
    translateButton = create(Label(canvas,image = translatephoto,bg=theme),2,55)
    defaultButtonFunctions(translateButton,lambda x:(Thread(target=grabScreen).start()))
    closeButton = create(Label(canvas,width=4,text="Exit",bg=theme,fg="white"),4,160)
    defaultButtonFunctions(closeButton,lambda x:window.destroy())
    move(canvas)

def setStarting(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    startingPoint = position()
    rectDrawingState = True
    if not rect:
       rect = canvas.create_rectangle(startingPoint[0], startingPoint[1],2,2, outline='red')

def setEnding(canvas):
    global startingPoint,rectDrawingState,rect,coords;
    if not rectDrawingState: return
    x,y=position()
    canvas.coords(rect,startingPoint[0], startingPoint[1], x,y)
    coords = [int(i) for i in (startingPoint[0]+1,startingPoint[1]+1,x-startingPoint[0]-1,y-startingPoint[1]-1)]
    
def drawingDone(canvas):
    global rectDrawingState,rect,coords;
    rectDrawingState = False
    canvas.delete(rect)
    canvas.destroy()
    rect = None

def on_double_click_release(func):
    global rectDrawingState;
    if rectDrawingState:
       func()

def on_release(canvas):
    drawingDone(canvas)
    window.attributes('-alpha', 1)
    window.config(cursor="arrow")
    window.update()
    text =image_to_string(screenshot(region=coords))
    print(text)
    textTranslation = translate(text).text
    translatePopup(text,textTranslation)

    
def grabScreen():
    canvas = create(Canvas(window,width = screen_width,height=screen_height),0,0)
    window.config(cursor="tcross")
    window.attributes('-alpha', 0.3)
    canvas.bind("<Double-Button-1>",lambda x:setStarting(canvas))
    canvas.bind("<B1-Motion>",lambda x:setEnding(canvas))
    canvas.bind("<ButtonRelease-1>",lambda x:on_double_click_release(lambda :on_release(canvas)))

setTheme("dark")
menuBar()
window.mainloop()


