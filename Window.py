import pickle
from tkinter import *
from tkinter import ttk
from LFSR import LFSR
from GeffeGenerator import GeffeGenerator
import timeit

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # Setting title
        self.master.title("Geffe Generator")
        # Allowing the widget to take full space of the root window
        self.pack(fill=BOTH, expand=1)
        # Creating tabs
        #   tabControl = ttk.Notebook(self)
        #   generatorTab = ttk.Frame(tabControl)
        #  infoTab = ttk.Frame(tabControl)
        #  tabControl.add(generatorTab, text="Generator")
        # tabControl.add(infoTab, text="Info")
        #  tabControl.pack(expan=1, fill="both")
        # Creating button
        submitButton = Button(self, text="Submit", command=self.buttonHandler)
        # Placing button
        submitButton.grid(column=5, row=2, padx=50)
        # Creating labels
        registerSizeLabel = Label(self, text="Enter the size of registers: ")
        outputSizeLabel = Label(self, text="Enter the size of generated key: ")
        initialRegister1Label = Label(self, text="Enter initial state of LFSR1: ")
        initialRegister2Label = Label(self, text="Enter initial state of LFSR2: ")
        initialRegister3Label = Label(self, text="Enter initial state of LFSR3: ")
        polynomial1Label = Label(self, text="Enter polynomial for LFSR1: ")
        polynomial2Label = Label(self, text="Enter polynomial for LFSR2: ")
        polynomial3Label = Label(self, text="Enter polynomial for LFSR3: ")
        writeToFileLabel = Label(self, text="Enter file path to save generated key: ")
        registerSizeLabel.grid(column=0, row=0)
        outputSizeLabel.grid(column=0, row=1)
        initialRegister1Label.grid(column=0, row=2)
        initialRegister2Label.grid(column=0, row=3)
        initialRegister3Label.grid(column=0, row=4)
        writeToFileLabel.grid(column=0, row=5)
        polynomial1Label.grid(column=3, row=2)
        polynomial2Label.grid(column=3, row=3)
        polynomial3Label.grid(column=3, row=4)

        # Creating entry fields
        self.registerSizeEntry = Entry(self)
        self.registerSizeEntry.grid(column=1, row=0)
        self.outputSizeEntry = Entry(self)
        self.outputSizeEntry.grid(column=1, row=1)
        self.register1Entry = Entry(self)
        self.register1Entry.grid(column=1, row=2)
        self.register2Entry = Entry(self)
        self.register2Entry.grid(column=1, row=3)
        self.register3Entry = Entry(self)
        self.register3Entry.grid(column=1, row=4)
        self.polynomial1Entry = Entry(self)
        self.polynomial1Entry.grid(column=4, row=2)
        self.polynomial2Entry = Entry(self)
        self.polynomial2Entry.grid(column=4, row=3)
        self.polynomial3Entry = Entry(self)
        self.polynomial3Entry.grid(column=4, row=4)
        self.filePathEntry = Entry(self)
        self.filePathEntry.grid(column=1, row=5)

        # Creating separator
        separator = ttk.Separator(self, orient=HORIZONTAL)
        separator.grid(column=0, row=6, sticky="we", pady=5, columnspan=6)

    def buttonHandler(self):
        # Generating registers
        pos = []
        lenthOfRegister = int(self.registerSizeEntry.get())
        sizeofoutput = int(self.outputSizeEntry.get())
        initial1 = self.register1Entry.get()

        binaryTable = [int(x) for x in bin(int(initial1))[2:].zfill(lenthOfRegister)]
        polynomial1= self.polynomial1Entry.get()
        z, o, t = polynomial1.split(",")
        pos.append(int(z))
        pos.append(int(o))
        pos.append(int(t))
        LFSR1 = LFSR(lenthOfRegister, binaryTable, pos)
        LFSR1T = LFSR1.makeLFSR(sizeofoutput)

        pos = []
        initial2 = int(self.register2Entry.get())
        binaryTable = [int(x) for x in bin(int(initial2))[2:].zfill(lenthOfRegister)]
        polynomial2 = self.polynomial2Entry.get()
        z, o, t = polynomial2.split(",")
        pos.append(int(z))
        pos.append(int(o))
        pos.append(int(t))
        LFSR2 = LFSR(lenthOfRegister, binaryTable, pos)
        LFSR2T = LFSR2.makeLFSR(sizeofoutput)

        pos = []
        initial3 = int(self.register3Entry.get())
        binaryTable = [int(x) for x in bin(int(initial3))[2:].zfill(lenthOfRegister)]
        polynomial3 = self.polynomial3Entry.get()
        z, o, t = polynomial3.split(",")
        pos.append(int(z))
        pos.append(int(o))
        pos.append(int(t))
        LFSR3 = LFSR(lenthOfRegister, binaryTable, pos)
        LFSR3T = LFSR3.makeLFSR(sizeofoutput)

        # Generating Geffe Generator output
        geffe = GeffeGenerator(LFSR1T, LFSR2T, LFSR3T)
        geffeT = geffe.generateGeffe(LFSR1T, LFSR2T, LFSR3T)
        strGeffe = str(geffeT)[2:-2]
        strGeffe = strGeffe.replace(", ", "")

        # Saving generated key in txt file
        path = self.filePathEntry.get()
        file = open(path, 'w')
        file.writelines(strGeffe)
        file.close()