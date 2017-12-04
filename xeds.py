'''
XEDS Utility
Michael J. McCaffrey

TODO:
ConRes and ConRelRes Scales
Instance Tab
Verify Tab
Visualize Tab?

'''
import os
import struct
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from tkinter import *
from tkinter import ttk, filedialog
from xml.dom import minidom

from bitstring import BitArray
version = 0.4

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

xelements = []

'''
Xelement: Describes an XEDS element, which could be a system, subsystem, sensor, etc. or a descriptive field
name: unique identifier for the element
bits: if a field, the number of bits needed to represent it
dataType: specifies type of data (UINT, ENUM, etc)
units: defines the unit for a field
isXeds: determines whether or not the element has sub-elements
parent: identifies the parent of the element
'''
class Xelement:
    treeId = 0
    frame = None
    label = None
    valueEntry = None

    def __init__(self, name, bits, dataType, units, isXeds, parent):
        self.parent = parent
        self.id = len(xelements)
        self.value = ''
        xelements.append(self)
        self.subXeds = []
        if parent is not None:
            self.parent.subXeds.append(self)
        if isXeds:
            self.data = [name, None, None, None, isXeds]
        else:
            self.data = [name, bits, dataType, units, isXeds]

    def makeField(self):
        self.valueEntry = Entry(self.frame, text=self.data[0].title())
        self.valueEntry.delete(0, END)
        self.valueEntry.insert(0,
                               self.data[1]
                               + " bit "
                               + self.data[2])
        if self.data[3] != '':
            self.valueEntry.insert(END,
                                   " ("
                                   + self.data[3]
                                   + ")")
        self.valueEntry.pack()
        self.frame.pack()

'''Create root Xelement called "Template". Update template tree'''
newTemplateRoot = Xelement("Template", 0, "", "", True, None)

'''*****************************************************************************************************'''
'''**********************************************XML STUFF**********************************************'''
'''*****************************************************************************************************'''


def exportX():
    if nb.index(nb.select()) == 0:
        exportXML()
    elif nb.index(nb.select()) == 1:
        exportXEDS()
    elif nb.index(nb.select()) == 2:
        return
    elif nb.index(nb.select()) == 3:
        return
    else:
        return


def importX():
    if nb.index(nb.select()) == 0:
        importXML(newTemplateRoot)
    elif nb.index(nb.select()) == 1:
        importTemplate(newInstanceRoot)
    elif nb.index(nb.select()) == 2:
        return
    elif nb.index(nb.select()) == 3:
        return
    else:
        return


'''
saveXML()
'''
def startXML(root):
    top = Element(root.data[0])
    buildXML(root, top)
    return top


def buildXML(xParent, parent):
    for subXeds in xParent.subXeds:
        if subXeds.data[4]:
            child = SubElement(parent, subXeds.data[0])
            buildXML(subXeds, child)
        else:
            child = SubElement(parent, subXeds.data[0],
                               {'bits': str(subXeds.data[1]),
                                'datatype': subXeds.data[2],
                                'units': subXeds.data[3],
                                })
            child.text = subXeds.value
            buildXML(subXeds, child)


def exportXML():
    directory = './xeds'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = filedialog.asksaveasfilename(initialdir=directory,
                                            title="Export XEDS",
                                            defaultextension=".xml",
                                            filetypes=([("xml", ".xml")]))
    print(prettify(startXML(newTemplateRoot)))
    file = open(filename, "w+")
    file.write(prettify(startXML(newTemplateRoot)))


def exportXEDS():
    directory = './xeds'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = filedialog.asksaveasfilename(initialdir=directory,
                                            title="Export XEDS",
                                            defaultextension=".xml",
                                            filetypes=([("xml", ".xml")]))
    print(prettify(startXML(newInstanceRoot)))
    file = open(filename, "w+")
    file.write(prettify(startXML(newInstanceRoot)))


def importXML(parent):
    directory = './xeds'
    if not os.path.exists(directory):
        os.makedirs(directory)
    master.filename = filedialog.askopenfilename(initialdir=directory,
                                                 title="Import XEDS",
                                                 filetypes=(("xml documents", "*.xml"), ("all files", "*.*")))
    importedTree = ElementTree.parse(master.filename)
    root = importedTree.getroot()
    templateTree.selection_set(newTemplateRoot.treeId)
    xelements.clear()
    newTemplateRoot.__init__("Template", 0, "", "", True, None)
    XMLtoXelement(root, newTemplateRoot)
    clearTemplateTree()
    updateTemplateTree(newTemplateRoot, '')


def XMLtoXelement(current, xparent):
        for child in current:
            if child.get('bits') is not None:
                xcurrent = Xelement(child.tag,
                                    child.get('bits'),
                                    child.get('datatype'),
                                    child.get('units'),
                                    False,
                                    xparent)
                if child.text is not None:
                    xcurrent.value = child.text
            else:
                xcurrent = Xelement(child.tag,
                                    '',
                                    '',
                                    '',
                                    True,
                                    xparent)

            #xcurrent.parent.subXeds.append(xcurrent)
            XMLtoXelement(child, xcurrent)


'''*****************************************************************************************************'''
'''*******************************************TREE VIEW STUFF*******************************************'''
'''*****************************************************************************************************'''

def moveElementUp(xelement):
    pos = xelement.parent.subXeds.index(xelement)
    if pos > 0:
        temp = xelement.parent.subXeds[pos]
        xelement.parent.subXeds[pos - 1] = xelement
        xelement.parent.subXeds[pos] = temp
        clearTemplateTree()
        updateTemplateTree(newTemplateRoot, '')
    return


def moveElementDown(xelement):
    pos = xelement.parent.subXeds.index(xelement)
    if pos < len(xelement.parent.subXeds) - 1:
        temp = xelement.parent.subXeds[pos]
        xelement.parent.subXeds[pos + 1] = xelement
        xelement.parent.subXeds[pos] = temp
        clearTemplateTree()
        updateTemplateTree(newTemplateRoot, '')
    return


'''
clearTemplateTree()
Erases the template tree view in preparation for rebuilding it with updates
'''
def clearTemplateTree():
    for child in templateTree.get_children():
        templateTree.delete(child)

        '''
        updateTemplateTree(xelement, parent)
        Populate the tree view with the contents of the Xelement tree
        xelement: The current node to be inserted
        parent: The parent node of the current node
        '''


def updateTemplateTree(xelement, parent):
    if not xelement.data[4]:
        xelement.treeId = templateTree.insert(parent, 'end', text=xelement.data[0],
                                              open=True, values=(xelement.data[1],
                                                                 xelement.data[2],
                                                                 xelement.data[3],
                                                                 xelement.id))
    else:
        xelement.treeId = templateTree.insert(parent, 'end', text=xelement.data[0],
                                              open=True, values=('',
                                                                 '',
                                                                 '',
                                                                 xelement.id))
        for subx in xelement.subXeds:
            updateTemplateTree(subx, xelement.treeId)


'''*****************************************************************************************************'''
'''********************************************XELEMENT STUFF*******************************************'''
'''*****************************************************************************************************'''


def removeSelectedElement(xelement):
    '''
    removeSelectedElement(xelement)
    Removes xelement from the tree.
    :param xelement:
    :return:
    '''
    xelement.parent.subXeds.remove(xelement)
    clearTemplateTree()
    updateTemplateTree(newTemplateRoot, '')


def addTemplateElementButton(parent):
    name = eElemName.get()
    bits = eElemBits.get()
    dataType = elementType.get()
    units = eElemUnits.get()
    addTemplateElement(parent, name, bits, dataType, units)


def addTemplateElement(parent, name, bits, dataType, units):

    '''
    addTemplateElement(parent)
    Creates a new Xelement with parameters as set in the GUI.
    Inserts the new Xelement into the Xelement tree under the parent node
    parent: The desired parent node of the new Xelement

    :param parent:
    :param name:
    :param bits:
    :param dataType:
    :param units:
    :return:
    '''

    xelement = Xelement(name, bits, dataType, units, xedsCheck.get(), parent)

    eElemName.delete(0, END)
    eElemBits.delete(0, END)
    elementType.set("uint")
    eElemUnits.delete(0, END)
    clearTemplateTree()
    updateTemplateTree(newTemplateRoot, '')
    templateTree.selection_set(parent.treeId)
    addElementFrame.focus(eElemName)

    return xelement


'''*****************************************************************************************************'''
'''********************************************MAIN GUI STUFF*******************************************'''
'''*****************************************************************************************************'''


def disableInputs(*args):
    for input in args:
        if type(input).__name__ == "OptionMenu":
            elementType.set("----")
        else:
            input.delete(0, END)

        input.config(state=DISABLED)


def enableInputs(*args):
    for input in args:
        if type(input).__name__ == "OptionMenu":
            elementType.set("uint")
        input.config(state=NORMAL)


def toggleInputs():
    if xedsCheck.get():
        disableInputs(eElemUnits, eElemBits, typeMenu)
    else:
        enableInputs(eElemUnits, eElemBits, typeMenu)


'''Construct the master GUI element.'''
master = Tk()

'''Set GUI width/height'''
master.geometry("800x640")

'''Set GUI Title'''
master.title('XEDS Utility ' + str(version))

'''
Construct a notebook (necessary for tabs).
Construct tabs. Arguments designate parent.
'''
nb = ttk.Notebook()
instanceTab = ttk.Frame(nb)
checkTab = ttk.Frame(nb)
templateTab = ttk.Frame(nb)

'''Add tabs to notebook and pack notebook'''
nb.add(templateTab, text="Build Template")
nb.add(instanceTab, text="Create/Edit XEDS")
nb.add(checkTab, text="Check System")
nb.pack(fill=BOTH, expand=1)


'''*****************************************************************************************************'''
'''********************************************BITSTREAM STUFF******************************************'''
'''*****************************************************************************************************'''

def BitStream(root):

    stream = ''
    for xelement in xelements:
        if xelement.data[2] != "char5" and xelement.value != '':
            temp = int(xelement.value)
            if not xelement.data[4]:
                if xelement.data[1] != '':
                    for n in range(int(xelement.data[1])):
                        if temp & 1:
                            stream += '1'
                        else:
                            stream += '0'
                        temp = temp >> 1

    return BitArray(bin=stream)


def exportStream():
    directory = './xeds'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = filedialog.asksaveasfilename(initialdir=directory,
                                            title="Export XEDS",
                                            defaultextension=".xeds",
                                            filetypes=([("XEDS", ".xeds")]))

    file = open(filename, "wb")
    stream = BitStream(newInstanceRoot)
    stream.tofile(file)


'''*****************************************************************************************************'''
'''***************************************TEMPLATE TOOLS GUI STUFF**************************************'''
'''*****************************************************************************************************'''

'''Build top menu for template tab'''
templateMenu = Menu(templateTab)
fileMenu = Menu(templateMenu, tearoff=0)
fileMenu.add_command(label="Import XML", command=importX)
fileMenu.add_command(label="Export XML", command=exportX)
fileMenu.add_command(label="Export Bitstream", command=exportStream)
templateMenu.add_cascade(label="File", menu=fileMenu)
master.config(menu=templateMenu)

'''Create and configure treeview for template tab.'''
templateTree = ttk.Treeview(templateTab, columns=("#1", "#2", "#3", "#4", "#5"))
templateTree["displaycolumns"] = ("#1", "#2", "#3")
templateTree.heading("#0", text="Property/Element")
templateTree.heading("#1", text="Bits")
templateTree.heading("#2", text="Data Type")
templateTree.heading("#3", text="Units")
templateTree.column('#0', stretch="false", minwidth=400, width=400)
templateTree.column('#1', stretch="false", minwidth=50, width=50, anchor=E)
templateTree.column('#2', stretch="false", minwidth=100, width=100, anchor=E)
templateTree.column('#3', stretch="false", minwidth=100, width=100, anchor=E)

'''Configure Scrollbar'''
templateScroll = ttk.Scrollbar(templateTree, command=templateTree.yview)
templateTree.configure(yscrollcommand=templateScroll.set, selectmode='browse', takefocus='true')
templateScroll.pack(fill=BOTH, side=RIGHT)

''' Pack template treeview'''
templateTree.pack(fill=BOTH, expand=1, pady=0, padx=10)

'''Create divider within template tab'''
newElementFrame = Frame(templateTab)

'''Create input field for element name'''
nameFrame = Frame(newElementFrame)
eElemName = Entry(nameFrame)
lElemName = Label(nameFrame, text="Property/Element: ")
lElemName.pack(pady=(0, 2))
eElemName.pack(pady=(2, 0))
eElemName.delete(0, END)
eElemName.insert(0, "")
nameFrame.pack(side=LEFT, padx=20)

'''Create input field for element bits'''
bitFrame = Frame(newElementFrame)
eElemBits = Entry(bitFrame)
lElemBits = Label(bitFrame, text="Bits: ")
lElemBits.pack(pady=(0, 2))
eElemBits.pack(pady=(2, 0))
eElemBits.delete(0, END)
eElemBits.insert(0, "")
bitFrame.pack(side=LEFT, padx=20)

'''Create dropdown menu for element data type'''
typeFrame = Frame(newElementFrame)
dataTypes = [
    "uint",
    "int",
    "enum",
    "char5",
    "conres",
    "conrelres"
]

elementType = StringVar(typeFrame)
elementType.set(dataTypes[0])  # set default

typeMenu = OptionMenu(*(typeFrame, elementType) + tuple(dataTypes))
basefolder = os.path.dirname(__file__)
imagepath = os.path.join(basefolder, 'img/arrow.png')
arrow = PhotoImage(file=imagepath)
typeMenu.config(relief=RAISED, indicatoron=0, width=75, compound='right', image=arrow)
lTypeMenu = Label(typeFrame, text="Type: ")
lTypeMenu.pack(pady=(0, 0))
typeMenu.pack(pady=(0, 0))
typeFrame.pack(side=LEFT, padx=20)

'''Create input field for element units'''
unitsFrame = Frame(newElementFrame)
eElemUnits = Entry(unitsFrame)
lElemUnits = Label(unitsFrame, text="Units:")
lElemUnits.pack(pady=(0, 2))
eElemUnits.pack(pady=(2, 0))
eElemUnits.delete(0, END)
eElemUnits.insert(0, "")
unitsFrame.pack(side=LEFT, padx=20)

'''Create checkbox for XEDS element'''
xedsCheck = IntVar()
checkFrame = Frame(newElementFrame)
subXCheck = Checkbutton(checkFrame, variable=xedsCheck, command=toggleInputs)
subXLabel = Label(checkFrame, text="subXEDS")
subXLabel.pack(side=LEFT)
subXCheck.pack(side=LEFT)
checkFrame.pack(side=LEFT, padx=20)

'''Create label for bottom pane'''
elemLabel = Label(templateTab, text="Add XEDS Element")
elemLabel.pack(side=TOP)

'''Pack input section'''
newElementFrame.pack()

'''Create frame division for submit button'''
addElementFrame = Frame(templateTab)

'''Button command calls function to add element data to template'''
bAddElement = Button(addElementFrame, text='Add Element', command=lambda: addTemplateElementButton(xelements[templateTree.item(templateTree.focus())['values'][3]]))

'''Pack button into frame division'''
bAddElement.pack(side=LEFT, padx=5)

'''Button command calls function to add element data to template'''
bAddElement = Button(addElementFrame, text='Remove Selected', command=lambda: removeSelectedElement(xelements[templateTree.item(templateTree.focus())['values'][3]]))

'''Pack button into frame division'''
bAddElement.pack(side=LEFT, padx=5)

addElementFrame.pack(pady=(5, 10))


'''*****************************************************************************************************'''
'''***************************************INSTANCE TOOLS GUI STUFF**************************************'''
'''*****************************************************************************************************'''


def importTemplate(parent):
    directory = './xeds'
    if not os.path.exists(directory):
        os.makedirs(directory)
    master.filename = filedialog.askopenfilename(initialdir=directory,
                                                 title="Import Template",
                                                 filetypes=(("xml documents", "*.xml"), ("all files", "*.*")))
    importedTree = ElementTree.parse(master.filename)
    root = importedTree.getroot()

    xelements.clear()
    clearFieldTree()
    newInstanceRoot.__init__("XEDS", 0, "", "", True, None)
    XMLtoXelement(root, newInstanceRoot)

    updateFieldTree(newInstanceRoot, '')


newInstanceRoot = Xelement("XEDS", 0, "", "", True, None)


def clearFieldTree():
    for child in instanceTree.get_children():
        instanceTree.delete(child)


def updateFieldTree(xelement, parent):
    if not xelement.data[4]:
        xelement.treeId = instanceTree.insert(parent, 'end', text=xelement.data[0],
                                              open=True, values=(xelement.value,
                                                                 xelement.data[2],
                                                                 xelement.data[3],
                                                                 xelement.id,
                                                                 '',
                                                                 xelement.data[1]))
    else:
        xelement.treeId = instanceTree.insert(parent, 'end', text=xelement.data[0],
                                              open=True, values=('',
                                                                 '',
                                                                 '',
                                                                 xelement.id))
        for subx in xelement.subXeds:
            updateFieldTree(subx, xelement.treeId)


'''Create and configure treeview for template tab.'''
instanceTree = ttk.Treeview(instanceTab, columns=("#1", "#2", "#3", "#4", "#5", "#6"))
instanceTree["displaycolumns"] = ("#1", "#6", "#2", "#3")
instanceTree.heading("#0", text="Property/Element")
instanceTree.heading("#2", text="Bits")
instanceTree.heading("#3", text="Data Type")
instanceTree.heading("#4", text="Units")
instanceTree.heading("#1", text="Value")
instanceTree.column('#1', stretch="false", minwidth=150, width=150)
instanceTree.column('#0', stretch="false", minwidth=350, width=350)
instanceTree.column('#2', stretch="false", minwidth=50, width=50, anchor=E)
instanceTree.column('#3', stretch="false", minwidth=100, width=100, anchor=E)
instanceTree.column('#4', stretch="false", minwidth=100, width=100, anchor=E)

'''Configure Scrollbar'''
instanceScroll = ttk.Scrollbar(instanceTree, command=instanceTree.yview)
instanceTree.configure(yscrollcommand=instanceScroll.set, selectmode='browse', takefocus='false')
instanceScroll.pack(fill=BOTH, side=RIGHT)

''' Pack template treeview'''
instanceTree.pack(fill=BOTH, expand=1, pady=0, padx=10)

'''Create divider within template tab'''
instanceFrame = Frame(instanceTab)

'''Pack input section'''
instanceFrame.pack()

'''Create frame diviasion for submit button'''
instanceButtonFrame = Frame(instanceTab)

eValueSet = Entry(instanceButtonFrame)
lValueSet = Label(instanceButtonFrame, text="Field Value")
lValueSet.pack()
eValueSet.pack()


def commitValue(*arg):
    index = instanceTree.item(instanceTree.selection())['values'][3]
    xelements[instanceTree.item(instanceTree.selection())['values'][3]].value = eValueSet.get()
    clearFieldTree()
    updateFieldTree(newInstanceRoot, '')
    if arg == 'shift':
        instanceTree.selection_set(xelements[index-1].treeId)

    else:
        instanceTree.selection_set(xelements[index + 1].treeId)

    eValueSet.delete(0, END)
    print(BitStream(newInstanceRoot))
    #instanceButtonFrame.focus_set(eValueSet)


instanceButtonFrame.pack(pady=(5, 10))


'''*****************************************************************************************************'''
'''********************************************RUNTIME STUFF********************************************'''
'''*****************************************************************************************************'''


def returnKey(event, *arg):
    if nb.index(nb.select()) == 0:
        addTemplateElementButton(xelements[templateTree.item(templateTree.selection())['values'][3]])
    elif nb.index(nb.select()) == 1:
        commitValue(arg)
    elif nb.index(nb.select()) == 2:
        return
    elif nb.index(nb.select()) == 3:
        return
    else:
        return


master.bind('<Return>', returnKey)
master.resizable(0, 0)

updateTemplateTree(newTemplateRoot, '')
mainloop()
