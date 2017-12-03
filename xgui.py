from tkinter import *
from tkinter import ttk
import os


class XMainApp:
    def __init__(self, w, h, title, version):
        self.app = Tk()
        self.app.geometry(str(w) + "x" + str(h))
        self.app.title(title + " " + version)


class XNotebook:
    def __init__(self):
        self.book = ttk.Notebook()


class XTab:
    def __init__(self, parent, tabtext):
        self.tab = Frame(parent)
        parent.add(self.tab, text=tabtext)

    def put(self):
        self.tab.pack(fill=BOTH, expand=1)


class XMenu:
    def __init__(self, parent, menutype, text, *args):
        self.menu = Menu(parent, tearoff=0)
        if menutype == "cascade":
            parent.add_cascade(label=text, menu=self.menu)
        elif menutype == "command":
            parent.add_command(label=text, command=args)
        elif menutype == "top":
            parent.config(menu=self.menu)


class XTemplateTree:
    def __init__(self, parent):
        self.tree = ttk.Treeview(parent, columns=("#1", "#2", "#3", "#4", "#5"))
        self.tree["displaycolumns"] = ("#1", "#2", "#3")
        self.tree.heading("#0", text="Property/Element")
        self.tree.heading("#1", text="Bits")
        self.tree.heading("#2", text="Data Type")
        self.tree.heading("#3", text="Units")
        self.tree.column('#0', stretch="false", minwidth=400, width=400)
        self.tree.column('#1', stretch="false", minwidth=50, width=50, anchor=E)
        self.tree.column('#2', stretch="false", minwidth=100, width=100, anchor=E)
        self.tree.column('#3', stretch="false", minwidth=100, width=100, anchor=E)
        self.scroll = ttk.Scrollbar(self.tree, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set, selectmode='browse', takefocus='true')
        self.scroll.pack(fill=BOTH, side=RIGHT)

    def put(self):
        self.tree.pack(fill=BOTH, expand=1, pady=0, padx=10)


class XInputFrame:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.put()

    inputs = []

    def populate(self):
        for inp in self.inputs:
            inp.put()

    def put(self, **kwargs):
        self.frame.pack(**kwargs)


class XInput:
    def __init__(self, parent, label, style, *args):
        self.parent = parent
        print(style.__name__)
        #parent.inputs.append(self)
        if style.__name__ == "Entry":
            self.field = style(parent)
            self.field.delete(0, END)
            self.field.insert(0, "")
        elif style.__name__ == "OptionMenu":
            basefolder = os.path.dirname(__file__)
            imagepath = os.path.join(basefolder, 'img/arrow.png')
            self.arrow = PhotoImage(file=imagepath)
            self.dropopts = args
            self.dropchoice = StringVar(parent)
            self.dropchoice.set(self.dropopts[0])  # set default
            self.field = OptionMenu(*(parent, self.dropchoice) + tuple(self.dropopts))
            self.field.config(relief=RAISED, indicatoron=0, width=75, compound='right', image=self.arrow)
        elif style.__name__ == "Checkbutton":
            self.var = IntVar()
            self.field = Checkbutton(parent, variable=self.var)
        else:
            self.field = style(parent)
        self.label = Label(parent, text=label)
        self.treeId = self.put()

    def put(self):
        self.label.pack()
        treeId = self.field.pack()
        return treeId


class XButton:
    def __init__(self, parent, label, action):
        self.field = Button(parent, text=label, command=lambda: action)
        self.put()

    def put(self):
        self.field.pack(side=LEFT, padx=5)
