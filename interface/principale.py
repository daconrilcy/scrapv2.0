from tkinter import *
from interface.default import Fenetredefault


class Principale:
    mainApp = None

    def __init__(self):
        self.mainApp = Fenetredefault()

    def mainloop(self):
        self.mainApp.mainloop()
