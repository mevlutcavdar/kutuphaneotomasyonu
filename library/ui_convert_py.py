from PyQt5 import uic

with open("main_window.py","w", encoding="utf-8") as fout:
    uic.compileUi("main_window.ui",fout)
with open("officer_window.py","w", encoding="utf-8") as fout:
    uic.compileUi("officer_window.ui",fout)
with open("User_window.py","w", encoding="utf-8") as fout:
    uic.compileUi("User_window.ui",fout)