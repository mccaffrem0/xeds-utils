''' 
XEDS Utility
Michael J. McCaffrey
'''
import xml.etree.ElementTree as etree
from tkinter import *
from tkinter import ttk

hierarchy = []

class Xelement:
    def __init__(self, name, bits, type, units, isXeds, parent):

        self.parent = parent;
        self.id = len(hierarchy)
        hierarchy.append(self)
        self.subXeds = []
        if isXeds:
            self.data = [name, None, None, None, isXeds]
        else:
            self.data = [name, bits, type, units, isXeds]



def clearTemplateTree():
    for child in templateTree.get_children():
        templateTree.delete(child)


def updateTemplateTree(xelement, parent):
    if not xelement.data[4]:
        templateTree.insert(parent, 'end', xelement.data[0], values=(xelement.data[0], xelement.data[1],
                                                                     xelement.data[2], xelement.data[3], xelement.id))
        templateTree.item(xelement.data[0], open=True)
    else:
        templateTree.insert(parent, 'end', xelement.data[0], values=(xelement.data[0], '', '', '', xelement.id))
        templateTree.item(xelement.data[0], open=True)
        for subx in xelement.subXeds:
            updateTemplateTree(subx, xelement.data[0])


def addTemplateElement(parent):
    print(templateTree.item(templateTree.focus())['values'])
    name = eElemName.get()
    bits = eElemBits.get()
    type = elementType.get()
    units = eElemUnits.get()

    xelement = Xelement(name, bits, type, units, xedsCheck.get(), parent)
    xelement.parent.subXeds.append(xelement)

    eElemName.delete(0, END)
    eElemBits.delete(0, END)
    elementType.set("UINT")
    eElemUnits.delete(0, END)
    clearTemplateTree()
    updateTemplateTree(newTemplateRoot, '')


master = Tk()

nb = ttk.Notebook()
create_tab = ttk.Frame(nb)
check_tab = ttk.Frame(nb)
template_tab = ttk.Frame(nb)

master.geometry("600x576")
master.title('XEDS Utility 0.1')

nb.add(template_tab, text="Build Template")
nb.add(create_tab, text="Create/Edit XEDS")
nb.add(check_tab, text="Check System")

nb.pack(fill=BOTH, expand=1)

templateTree = ttk.Treeview(template_tab, columns=("#1", "#2", "#3", "#4", "#5"))
templateTree["displaycolumns"] = ("#1", "#2", "#3", "#4")
templateTree.heading("#1", text="Property/Element")
templateTree.heading("#2", text="Bits")
templateTree.heading("#3", text="Data Type")
templateTree.heading("#4", text="Units")
templateTree.column('#0', stretch="false", minwidth=20, width=20)
templateTree.column('#1', stretch="false", minwidth=250, width=250, anchor=W)
templateTree.column('#2', stretch="false", minwidth=50, width=50, anchor=E)
templateTree.column('#3', stretch="false", minwidth=100, width=100, anchor=E)
templateTree.column('#4', stretch="false", minwidth=100, width=100, anchor=E)

templateScroll = ttk.Scrollbar(templateTree, command=templateTree.yview)
templateTree.configure(yscrollcommand=templateScroll.set, selectmode='browse', takefocus='true')
templateScroll.pack(fill=BOTH, side=RIGHT)
templateTree.pack(fill=BOTH, expand=1, pady=0, padx=10)

newElementFrame = Frame(template_tab)

nameFrame = Frame(newElementFrame)
eElemName = Entry(nameFrame)
lElemName = Label(nameFrame, text="Property/Element: ")
lElemName.pack(pady=(0, 2))
eElemName.pack(pady=(2, 0))
eElemName.delete(0, END)
eElemName.insert(0, "")
nameFrame.pack(side=LEFT, padx=20)

bitFrame = Frame(newElementFrame)
eElemBits = Entry(bitFrame)
lElemBits = Label(bitFrame, text="Bits: ")
lElemBits.pack(pady=(0, 2))
eElemBits.pack(pady=(2, 0))
eElemBits.delete(0, END)
eElemBits.insert(0, "")
bitFrame.pack(side=LEFT, padx=20)

typeFrame = Frame(newElementFrame)
dataTypes = [
    "UINT",
    "INT",
    "ENUM",
    "CHAR5",
    "ConRes",
    "ConRelRes"
]

elementType = StringVar(typeFrame)
elementType.set(dataTypes[0])  # set default

typeMenu = OptionMenu(*(typeFrame, elementType) + tuple(dataTypes))
lTypeMenu = Label(typeFrame, text="Type: ")
lTypeMenu.pack(pady=(0, 2))
typeMenu.pack(pady=(2, 0))
typeFrame.pack(side=LEFT, padx=20)

unitsFrame = Frame(newElementFrame)
eElemUnits = Entry(unitsFrame)
lElemUnits = Label(unitsFrame, text="Units:")
lElemUnits.pack(pady=(0, 2))
eElemUnits.pack(pady=(2, 0))
eElemUnits.delete(0, END)
eElemUnits.insert(0, "")
unitsFrame.pack(side=LEFT, padx=20)

xedsCheck = IntVar()
elemLabelFrame = Frame(template_tab)
subXCheck = Checkbutton(elemLabelFrame, text="subXEDS", variable=xedsCheck)
elemLabel = Label(template_tab, text="Add XEDS Element")
subXCheck.pack(side=LEFT)
elemLabel.pack(side=TOP)
elemLabelFrame.pack()

newElementFrame.pack()

addElementFrame = Frame(template_tab)
bAddElement = Button(addElementFrame, text='Add Element', command=lambda: addTemplateElement(hierarchy[templateTree.item(templateTree.focus())['values'][4]]))
bAddElement.pack()
addElementFrame.pack(pady=(5, 0))
addElementFrame.config(bg="red")

newTemplateRoot = Xelement("Template", 0, "", "", True, None)
updateTemplateTree(newTemplateRoot, '')

mainloop()