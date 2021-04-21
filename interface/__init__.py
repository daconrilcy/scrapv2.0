from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from events import Events


class Fenetredefault(Tk):
    iconeMain = "interface/scrapper_32.ico"
    geom = "1024x768"
    min_x = 640
    min_y = 400
    titretex = "scrapy"
    bgcolor = '#161616'
    mainFrame = None
    menuBar = None
    eventsManager = None
    bt = None
    lb = None
    n = 1
    framePage = {}
    pagesNames = []
    pos_x = 0
    pos_y = 0
    pageEncours: Frame
    arial18 = None
    color_gris = []
    arial = []
    default_font = None
    marques = ['Gigabyte', 'Asus', 'MSI', 'EVGA']
    sources = ['file', 'web']
    etapes = ['import', 'conversion', 'check',"upload"]

    def __init__(self, eventsManager: Events):
        Tk.__init__(self)
        self.eventsManager = eventsManager
        self.preparameters()
        self.defineWindows()
        self.createMenu()
        self.createPages()
        self.pageEncours = self.framePage['acceuil']

    def preparameters(self):
        screenx = int(self.winfo_screenwidth())
        screeny = int(self.winfo_screenheight())
        widthP = screenx * 3 // 4
        heightP = screeny * 3 // 4

        self.pos_x = (screenx // 2) - (widthP // 2)
        self.pos_y = (screeny // 2) - (heightP // 2)
        self.geom = "{}x{}+{}+{}".format(widthP, heightP, self.pos_x, self.pos_y)
        self.defcolor()
        self.defFont()

    def defcolor(self):
        for i in range(0, 257, 16):
            v = hex(i - 1)
            v = v[2::]
            self.color_gris.append("#" + v + v + v)
        self.bgcolor = self.color_gris[4]

    def defFont(self):
        for i in range(6, 36):
            self.arial.append({"normal": tkFont.Font(family='arial', size=i),
                               "bold": tkFont.Font(family='arial', size=i, weight='bold')})
        self.default_font = self.arial[8]["normal"]

    def defineWindows(self):
        self.geometry(self.geom)
        self.minsize(self.min_x, self.min_y)
        self.title(self.titretex)
        self.config(background=self.bgcolor)
        self.iconbitmap(self.iconeMain)

    def createMenu(self):
        menuBar = Menu(self)
        menuFile = Menu(menuBar, tearoff=0)
        menuFile.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="File", menu=menuFile)
        self.config(menu=menuBar)
        self.menuBar = menuBar

    def addPage(self, name: str, frame: Frame):
        self.framePage[name] = frame
        self.pagesNames.append(name)

    def createLisbox(self, frame: Frame, selectionmode: str, values: list, width: int):
        if selectionmode is None:
            selectionmode = 'single'
        if selectionmode == "":
            selectionmode = 'single'

        if width is None:
            width = 40
        if width == 0:
            width = 40

        lb = Listbox(frame, activestyle="none", cursor="hand1",
                     selectmode=selectionmode, width=width, exportselection=0,
                     bg=self.color_gris[4], fg='#FFFFFF'
                     )

        if values:
            if len(values) > 0:
                n = 0
                for v in values:
                    lb.insert(n, v)
                    n += 1

        return lb

    def recupSelectListBox(self, lb: Listbox):
        if len(lb.curselection()) == 0:
            return []
        else:
            brd = []
            for li in lb.curselection():
                brd.append(lb.get(li))
            return brd

    def openFileSource(self):
        filename = askopenfilename(
            parent=self,
            title="Ouvrir votre document",
            initialdir=r"./", filetypes=[('txt files', '.txt'), ('all files', '.*')]
        )
        try:
            with open(filename) as file:
                if file is not None:
                    self.fileSource.set(file.name)
                    print(self.fileSource.get())
        except BaseException:
            self.fileSource.set('')

    # Pages

    def createPages(self):
        self.createPageAccueil()
        self.createPageImport()

    def createPageAccueil(self):
        mainFrame = Frame(self, bg=self.bgcolor)

        topFrame = Frame(mainFrame, bg=self.color_gris[4], relief=GROOVE, bd=2)
        btFrame = Frame(mainFrame, bg=self.bgcolor)

        btQuit = Button(topFrame, bg=self.color_gris[4], fg="#FFFFFF", text="Quit", font=self.arial[2]["normal"],
                        pady=5, width=12,
                        command=self.quit)
        btStart = Button(topFrame, bg=self.color_gris[4], fg="#FFFFFF", text="Start", font=self.arial[2]["normal"],
                         pady=5, width=12,
                         command=self.startAction)
        btClear = Button(topFrame, bg=self.color_gris[4], fg="#FFFFFF", text="Clear", font=self.arial[2]["normal"],
                         pady=5, width=12,
                         command=self.clearSelection)


        self.fileSource = StringVar()
        self.fileSource.set("")

        lbl = Label(topFrame, textvariable=self.fileSource, justify='left', padx=5, bg=self.color_gris[4], relief=FLAT, fg="#FFFFFF")

        btSource = Button(topFrame, bg=self.color_gris[4], fg="#FFFFFF", text="Source", font=self.arial[2]["normal"],
                          pady=5, width=12,
                          command=self.openFileSource)

        btClear.pack(side=LEFT)
        btStart.pack(side=LEFT)
        btQuit.pack(side=LEFT)
        btSource.pack(side=LEFT)
        lbl.pack(side=LEFT)

        lb = self.createLisbox(frame=btFrame, selectionmode='multiple', values=self.marques, width=40)
        lb.select_set(0)
        self.lbMarque = lb

        lb2 = self.createLisbox(frame=btFrame, selectionmode='single', values=self.sources, width=40)
        lb2.select_set(1)
        self.lbsouces = lb2

        lb3 = self.createLisbox(frame=btFrame, selectionmode='multiple', values=self.etapes, width=40)
        lb3.select_set(1)
        self.lbetape = lb3

        self.lbMarque.pack(side=LEFT, padx=5, pady=5)
        self.lbsouces.pack(side=LEFT, padx=5, pady=5)
        self.lbetape.pack(side=LEFT, padx=5, pady=5)
        lbl.pack(side=LEFT)

        topFrame.pack(side=TOP, fill=X)
        btFrame.pack(side=TOP, fill=BOTH)
        mainFrame.pack(expand=YES, fill=BOTH)

        self.addPage("acceuil", mainFrame)

    def createPageImport(self):

        self.datasToLbl = StringVar()
        self.ActionToLb = StringVar()
        mainFrame = Frame(self, bg=self.bgcolor)

        topFrame = Frame(mainFrame, bg=self.bgcolor, padx=10, pady=10)
        btCommeBack = Button(topFrame, text="Back", bg=self.bgcolor,
                             fg="#FFFFFF", font=self.arial[4]['normal'], padx=5, pady=5)
        btStop = Button(topFrame, text="Stop", bg=self.bgcolor, fg="#FFFFFF",
                        font=self.arial[4]['normal'], padx=5, pady=5)
        btStop.pack(side=RIGHT)
        btCommeBack.pack(side=LEFT)

        bottomFrame = Frame(mainFrame, bg=self.bgcolor, padx=10, pady=10)
        btLeftFrame = Frame(bottomFrame, bg=self.bgcolor, padx=0, pady=0)
        btRigthFrame = Frame(bottomFrame, bg=self.bgcolor, padx=0, pady=0)

        lbTitreData = Label(btRigthFrame, bg=self.bgcolor, font=self.arial[18]['bold'],
                            fg="#FFFFFF", padx=5, pady=5, width=28,
                            text="Datas", justify=CENTER)
        lbTitreAction = Label(btLeftFrame, bg=self.bgcolor, font=self.arial[18]['bold'],
                              fg="#FFFFFF", padx=5, pady=5, width=28,
                              text="Action En Cours", justify=CENTER)
        lbDatas = Label(btRigthFrame, bg=self.color_gris[2], padx=5, pady=5, font=self.default_font,
                        fg="#FFFFFF", width=60, height=40,
                        textvariable=self.datasToLbl, justify=LEFT)
        lbActions = Label(btLeftFrame, bg=self.color_gris[2], padx=5, pady=5, font=self.default_font,
                          fg="#FFFFFF", width=60, height=40,
                          textvariable=self.ActionToLb, justify=LEFT)

        lbTitreData.pack(side=TOP)
        lbTitreAction.pack(side=TOP)
        lbDatas.pack(side=TOP)
        lbActions.pack(side=TOP)

        topFrame.pack(side=TOP, fill=X)

        btLeftFrame.pack(side=LEFT, fill=BOTH)
        btRigthFrame.pack(side=RIGHT, fill=BOTH)
        bottomFrame.pack(side=TOP, fill=BOTH)

        self.addPage("pageimport", mainFrame)

    def clearSelection(self):
        pass

    # Fonctions utlisant les routes

    def quit(self):
        """Quit the Tcl interpreter. All widgets will be destroyed."""
        self.eventsManager.add("Affich", "quit")
        self.tk.quit()

    def startAction(self):
        brd = self.recupSelectListBox(self.lbMarque)
        if len(brd) == 0:
            return
        origin = self.recupSelectListBox(self.lbsouces)
        if len(origin) == 0:
            return
        self.eventsManager.add("Affich", "importbrand", [origin, brd])

    # Fonctions appelable par les routes

    def affichpage(self, pageName: list):
        if len(pageName) == 0:
            return
        else:
            name = pageName[0]
        if self.pageEncours:
            self.pageEncours.pack_forget()
        self.framePage[name].pack(expand=YES, fill=BOTH)
        self.pageEncours = self.framePage[name]