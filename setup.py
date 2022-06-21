from os import system

system("windres my.rc -O coff -o my.res")
system("gcc my.res main.c -o translate.exe")
system("pip install -r requirements.txt")


