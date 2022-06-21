from googletrans import Translator
from keyboard import add_hotkey
from pywinauto import application
from csv import DictWriter   
from os import system
import pygetwindow as gw
win = gw.getActiveWindow()
c=0
fieldsnames=['sentence','translation']
translator = Translator()
app = application.Application().connect(handle=win._hWnd)
system("cls&mode 25,5")

def translate(sentence):
    return translator.translate(sentence,dest="tr")

def hotkeyFunction():
    global c
    c+=1
    app.top_window().set_focus()
    if c==2:
       win.minimize()
       c=0
       
def noteit(word,translation):
    with open('saved.csv', 'a+') as f:
         writer = DictWriter(f, fieldnames=fieldsnames)
         writer.writerow({'sentence':word,'translation':translation})
    return translation

add_hotkey('ctrl+ü',hotkeyFunction)
while 1:
    sentence = input("==>")
    print(noteit(sentence,translate(sentence).text))
    
#requirement.txt
"""
googletrans==3.1.0a0
keyboard==0.13.5
pywinauto==0.6.8
"""

