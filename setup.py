from os import system
from subprocess import PIPE,run

system_path=run(["path"], capture_output=True, text=True,shell=True).stdout.lower()
if "g++" and "mingw" in system_path:
    system("windres my.rc -O coff -o my.res")
    system("gcc my.res main.c -o translate.exe")
    system("pip install -r requirements.txt")

else:
     system("pip install pyinstaller")
     system("pip install -r requirements.txt")
     system("python pyinstaller translate.py --ico=icon.ico -F")
