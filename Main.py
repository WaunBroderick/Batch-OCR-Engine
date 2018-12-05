import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

#####################DO NOT REMOVE###############################
##                                                             ##
##          DEVELOPED BY WAUN BRODERICK & MUDIT SHARMA         ##
##     PERSONAL BANKING - PERFORMANCE INTEGRITY OPERATIONS     ##
##                                                             ##
##                         08/2018                             ##
##                                                             ##
##                RFI AUTOMATED INGESTION SYSTEM               ##
##                                                             ##
#####################DO NOT REMOVE###############################

#Local class imports
from Builder import *


#Tkinter Graphical assets
from tkinter import Tk, Label, Button, filedialog, messagebox
from tkinter.ttk import Progressbar
from tkinter import *

#Imports for the local classes, methods and functions within this file
from PIL import ImageTk, Image
import csv
import threading
import time

#Class responsible for building the graphical user interface for INPROD
class INPRODGUI:

    #Global defined variable for the scandir for extensible use
    def _global_scanDir_(self, arg1):
        global SCANSTR
        SCANSTR = arg1

    #Global defined variable for the outdir for extensible use
    def _global_outDir_(self, arg2):
        global OUTSTR
        OUTSTR = arg2

    # Global defined variable for the selection
    def _global_selection_(self, selection):
        global SELECTION
        SELECTION = selection

    #Initalization of the Tkinter GUI
    def __init__(self, master):
        #instantiate the object and name it
        self.master = master
        master.title("Inprod")
        #set selection default
        self._global_selection_("RFI")

        #Welcoming message label
        self.label = Label(master, text="Please select both a input directory and an output directory.")
        self.label.pack()

        #Scan directory button and placement
        self.inScan_button = Button(master, text="Select Scan Directory", command=self.scanDir)
        self.inScan_button.place(x=120,y=310)

        #Output directory button and placement
        self.outScan_button = Button(master, text="Select Output Directory", command=self.outDir)
        self.outScan_button.place(x=250,y=310)

        #Option variable for the dropdown menu
        option = StringVar(master)
        #Default option menu variable
        option.set("RFI")

        #Dropdown option menu options, the command triggered and the packing of the obj
        w = OptionMenu(master, option, "RFI","RESL", "Audit", command= self.selectionCallback)
        w.pack()

        #Variable check boxes for implemented Quality Control Measures
        CheckVar1 = IntVar()

        #Accuracy tuning checkbox
        C1 = Checkbutton(master, text="Accuracy Tuner", variable=CheckVar1, onvalue=1, offvalue=0, height=0, width=0)

        #
        C1.place(x=200,y=340)

        #
        self.trainFont_button = Button(master, text="Train Font", command=self.trainFont)
        self.trainFont_button.place(x=210,y=370)


        self.execute_button = Button(master, text="Execute", command=self.execute)
        self.execute_button.place(x=215,y=410)


        self.progress = Progressbar(master, orient=HORIZONTAL, length=350, mode='indeterminate')
        self.progress.place(x=85, y=460)

        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.place(x=230,y=500)

    def func(self, value):
        print(value)

    #Progress bar functionality
    def traitement(self):
        def real_traitement():
            self.progress.grid(row=1, column=0)
            self.progress.start()
            time.sleep(5)
            self.progress.stop()
            self.progress.grid_forget()

            self.btn['state'] = 'normal'

        self.btn['state'] = 'disabled'
        threading.Thread(target=real_traitement).start()
    #selecting the Scan directory functionality
    def scanDir(self):
        scanDir_selected = filedialog.askdirectory()
        self._global_scanDir_(scanDir_selected)

    #selecting the Out Directory functionality
    def outDir(self):
        outDir_selected = filedialog.askdirectory()
        self._global_outDir_(outDir_selected)

    #The functionality of the exectue button
    def execute(self):
        #Try catch exception on the !=null variables of the selected scan and output directory
        try:
            OUTSTR, SCANSTR
        except:
        #Basic message response on catch exception
            messagebox.showinfo("Missing Directory", "Please select a scan Directory and an output Directory before executing.")
        else:
        #True initalization on the builder file and class with the global variables selected
            init = Build()
            init._global_scanDir_(SCANSTR)
            init._global_outDir_(OUTSTR)
            init._global_selection_(SELECTION)
            #init._directories_(SCANSTR, OUTSTR, SELECTION)
            #init._clean_()
            init._img_to_txt_()
            sort = Sort()
            sort._english_subSorter_()

        if OUTSTR == '' or SCANSTR == '':
            print("please dont")

    #Implementing the font training functionality ======= PORT FROM DEVELOP REPOSITORY WHEN NEEDED============
    def trainFont(self):
        messagebox.showinfo("Font Trainer", "This option will allow you to select a file wit")


    def selectionCallback(self, selection):
        Selection = selection
        self._global_selection_(Selection)

#The class responsible for the final collection of processed documents and feeding of their output lists to respective CSVs
class Collector:
    #collector for english files
    def _english_collector(self, var_list, dstDir):
        #Directory and name of csv file for the output csv along with the variable list
        with open(dstDir + '/eng-final.csv', 'a') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(var_list)

    #collector for french files
    def _french_collector(self, var_list, dstDir):
        #Directory and name of csv file for the output csv along with the variable list
        with open(dstDir + '/fr-final.csv', 'a') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(var_list)

#Main Program Entry Point
if __name__ == '__main__':
    #Absolute file path to the tesseract engine
    pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'

    #Instantiate the GUI
    root = Tk()

    #GUI size and lock resizing
    root.minsize(500, 600)
    root.resizable(width=False, height=False)


    #INPROD Logo
    img = Image.open('./props/inprod-logo.png')
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.pack()


    #windowLogo
    root.iconbitmap(r'./props/favicon.ico')

    my_gui = INPRODGUI(root)
    root.mainloop()
