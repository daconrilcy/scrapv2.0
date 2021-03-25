from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class Fenetredefault(Tk):
    windows = None
    diminit = "1024x768"
    min_x = 800
    min_y = 900
    titretex = "scrapy"
    logopath = "interface/scrapper_32.ico"
    bgcolor = '#161616'
    mainFrame = None
    menuBar = None

    def __init__(self):
        Tk.__init__(self)
        self.defineWindows()
        self.createmainFrame()
        self.createMenu()

    def defineWindows(self):
        self.geometry(self.diminit)
        self.minsize(self.min_x, self.min_y)
        self.title(self.titretex, bg=self.bgcolor)
        self.iconbitmap(self.logopath)
        self.config(background= self.bgcolor)

    def createmainFrame(self):
        self.mainFrame = Frame(self.windows, bg=self.bgcolor)
        self.mainFrame.pack(expand=YES)

    def createMenu(self):
        menuBar = Menu(self)
        menuFile = Menu(menuBar, tearoff=0)
        menuFile.add_command(label="Nouveau", command=self.doSomething)
        menuFile.add_command(label="Ouvrir", command=self.openFile)
        menuFile.add_command(label="Sauvegarder", command=self.doSomething)
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="File", menu=menuFile)

        menuEdit = Menu(menuBar, tearoff=0)
        menuEdit.add_command(label="Undo", command=self.doSomething)
        menuEdit.add_separator()
        menuEdit.add_command(label="Copy", command=self.doSomething)
        menuEdit.add_command(label="Cut", command=self.doSomething)
        menuEdit.add_command(label="Paste", command=self.doSomething)
        menuBar.add_cascade(label="Edit", menu=menuEdit)

        menuHelp = Menu(menuBar, tearoff=0)
        menuHelp.add_command(label="About", command=self.doAbout)
        menuBar.add_cascade(label="Help", menu=menuHelp)

        self.config(menu=menuBar)
        self.menuBar = menuBar

    def openFile(self):
        file = askopenfilename(title="Choose the file to open",
                               filetypes=[("PNG image", ".png"), ("GIF image", ".gif"), ("All files", ".*")])
        print(file)

    def doSomething(self):
        print("Menu clicked")

    def doAbout(self):
        messagebox.showinfo("My title", "My message")