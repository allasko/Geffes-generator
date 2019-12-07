from tkinter import *
from tkinter import ttk
from LFSR import LFSR
from GeffeGenerator import GeffeGenerator

def strxor(a, b):  # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # Setting title
        self.master.title("Geffe's Generator")
        # Allowing the widget to take full space of the root window
        self.pack(fill=BOTH, expand=1)
        # Creating button
        submitButton = Button(self, text="Submit", command=self.buttonHandler)
        decipherButton = Button(self, text="Decipher", command=self.decipherHandler)
        # Placing button
        submitButton.grid(column=5, row=2, padx=50)
        decipherButton.grid(column=5, row=8)
        # Creating labels
        registerSizeLabel = Label(self, text="Enter the size of three registers: ")
        outputSizeLabel = Label(self, text="Enter the size of generated key: ")
        initialRegister1Label = Label(self, text="Enter initial state of LFSR1: ")
        initialRegister2Label = Label(self, text="Enter initial state of LFSR2: ")
        initialRegister3Label = Label(self, text="Enter initial state of LFSR3: ")
        polynomial1Label = Label(self, text="Enter polynomial for LFSR1: ")
        polynomial2Label = Label(self, text="Enter polynomial for LFSR2: ")
        polynomial3Label = Label(self, text="Enter polynomial for LFSR3: ")
        writeToFileLabel = Label(self, text="Enter file path to save generated key: ")
        openFileLabel = Label(self, text="Enter path to the file you want to open: ")
        secretLabel = Label(self, text="Cryptogram: ")
        clearTextLabel = Label(self, text="Clear text: ")
        keyPathLabel = Label(self, text="Enter path to generated key: ")
        registerSizeLabel.grid(column=0, row=0)
        outputSizeLabel.grid(column=0, row=1)
        initialRegister1Label.grid(column=0, row=2)
        initialRegister2Label.grid(column=0, row=3)
        initialRegister3Label.grid(column=0, row=4)
        writeToFileLabel.grid(column=0, row=5)
        polynomial1Label.grid(column=3, row=2)
        polynomial2Label.grid(column=3, row=3)
        polynomial3Label.grid(column=3, row=4)
        openFileLabel.grid(column=0, row=6)
        secretLabel.grid(column=0, row=7, columnspan=2)
        clearTextLabel.grid(column=2, row=7, columnspan=2)
        keyPathLabel.grid(column=3, row=5)
        # Creating entry fields
        self.registerSizeEntry = Entry(self)
        self.registerSizeEntry.grid(column=1, row=0)
        self.registerSizeEntry2 = Entry(self)
        self.registerSizeEntry2.grid(column=2, row=0)
        self.registerSizeEntry3 = Entry(self)
        self.registerSizeEntry3.grid(column=3, row=0)
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
        self.openFileEntry = Entry(self)
        self.openFileEntry.grid(column=1, row=6)
        self.keyPathEntry = Entry(self)
        self.keyPathEntry.grid(column=4, row=5)
        self.infoEntry = Text(self, height=20, width=30, wrap=WORD)
        self.infoEntry.grid(column=7, row=8, pady=5, columnspan=3)
        # self.photoEntry = Text(self, height=20, width=40)
        # self.photoEntry.grid(column=0, row=7, columnspan=2)
        self.secretEntry = Text(self, height=20, width=40, wrap=CHAR)
        self.secretEntry.grid(column=0, row=8, columnspan=2)
        self.clearTextEntry = Text(self, height=20, width=40, wrap=WORD)
        self.clearTextEntry.grid(column=3, row=8, columnspan=2)
        # # Creating separator
        # separator = ttk.Separator(self, orient=HORIZONTAL)
        # separator.grid(column=0, row=6, sticky="we", pady=5, columnspan=6)
        # # Adding photo
        # self.image = PhotoImage(file="image.gif")
        # self.photoEntry.insert(END, "\n")
        # self.photoEntry.image_create(END, image=self.image)
        # # Adding Scrollbar
        # self.scroll = Scrollbar(self, command=self.infoEntry.yview)
        # self.infoEntry.configure(yscrollcommand=self.scroll.set)
        # self.scroll.grid(column=6, row=7, rowspan=10, sticky="ns")
        ## Creating info
        self.infoEntry.tag_configure('big', font=('Verdana', 16, 'bold'))
        self.infoEntry.tag_configure('info', font=('Arial',12))
        self.infoEntry.insert(INSERT, 'Geffe\'s Generator\n', 'big')
        info = """\nGenerator was invented in 1973 by P.R Geffe. Consists of three LFSRs: LFSR-1, LFSR-2 and LFSR-3. If we denote the outputs of these registers by a1, a2 and a3, respectively, then the Boolean function that combines the three registers to provide the generator output is given by k = ((a1 and a3) or (not(a1)and a2))"""
        self.infoEntry.insert(END, info, 'info')
        use = """\n\n To use this generator you need to enter the size of registers, the length of generated key, initial values for all three registers and polynomials for each register. To save the output in the file you need to add path to this file."""
        self.infoEntry.insert(END, use, 'info')
        bounds = """\n\n Maximum length of the register is 1024 bit."""
        self.infoEntry.insert(END, bounds, 'info')
    def buttonHandler(self):
        global secret, strGeffe

        # Opening file with text
        openPath = self.openFileEntry.get()
        oFile = open(openPath, "r")
        content = oFile.read()

        if(not self.keyPathEntry.get()):
            # Generating registers
            # Creating LFSR1
            pos = []
            lenthOfRegister1 = int(self.registerSizeEntry.get())
            sizeofoutput = int(self.outputSizeEntry.get())
            initial1 = self.register1Entry.get()
            binaryTable = [int(x) for x in bin(int(initial1))[2:].zfill(lenthOfRegister1)]
            polynomial1= self.polynomial1Entry.get()
            z, o, t = polynomial1.split(",")
            pos.append(int(z))
            pos.append(int(o))
            pos.append(int(t))
            LFSR1 = LFSR(lenthOfRegister1, binaryTable, pos)
            LFSR1T = LFSR1.makeLFSR(sizeofoutput)
            # Creating LFSR2
            pos = []
            lenthOfRegister2 = int(self.registerSizeEntry2.get())
            initial2 = int(self.register2Entry.get())
            binaryTable = [int(x) for x in bin(int(initial2))[2:].zfill(lenthOfRegister2)]
            polynomial2 = self.polynomial2Entry.get()
            z, o, t = polynomial2.split(",")
            pos.append(int(z))
            pos.append(int(o))
            pos.append(int(t))
            LFSR2 = LFSR(lenthOfRegister2, binaryTable, pos)
            LFSR2T = LFSR2.makeLFSR(sizeofoutput)
            # Creating LFSR3
            pos = []
            lenthOfRegister3 = int(self.registerSizeEntry3.get())
            initial3 = int(self.register3Entry.get())
            binaryTable = [int(x) for x in bin(int(initial3))[2:].zfill(lenthOfRegister3)]
            polynomial3 = self.polynomial3Entry.get()
            z, o, t = polynomial3.split(",")
            pos.append(int(z))
            pos.append(int(o))
            pos.append(int(t))
            LFSR3 = LFSR(lenthOfRegister3, binaryTable, pos)
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
            # XOR on text and key
            secret = strxor(content, strGeffe)
            self.secretEntry.insert(END, secret)
        elif(self.keyPathEntry.get()):

            openKeyPath = self.keyPathEntry.get()
            oKey = open(openKeyPath,"r")
            strGeffe = oKey.read()
            secret = strxor(content,strGeffe)
            self.secretEntry.insert(END, secret)
        return secret, strGeffe

    def decipherHandler(self):
        # Deciphering cryptogram
        output = strxor(secret, strGeffe)
        self.clearTextEntry.insert(END, output)
