#####################DO NOT REMOVE###############################
##                                                             ##
##          DEVELOPED BY WAUN BRODERICK & MUDIT SHARMA         ##
##     PERSONAL BANKING - PERFORMANCE INTEGRITY OPERATIONS     ##
##                                                             ##
##                         08/208                              ##
##                                                             ##
##                RFI AUTOMATED INGESTION SYSTEM               ##
##                                                             ##
#####################DO NOT REMOVE###############################

#Local class imports
from Router import *
from Tuner import *

#Imports for the local classes, methods and functions within this file
import os.path
from wand.image import Image as wi
import pytesseract
import re
import PIL.Image
import io
import shutil

#Class responsible for the bulk of building directories, passing, cloning, converting and amalgamating files
class Build():

    def __init__(self):
        global tuner
        global Sorter
        tuner = QC()
        Sorter = Sort()

    #Global defined variable for the scandir for extensible use
    def _global_scanDir_(self, _scanDir):
        global SCANSTR
        SCANSTR = _scanDir

    #Global defined variable for the outdir for extensible use
    def _global_outDir_(self, _outDir):
        global OUTSTR
        OUTSTR = _outDir

    # Global defined variable for the selection
    def _global_selection_(self, _selection):
        global SELECTION
        SELECTION = _selection

    #Creates the directories and folder paths for preceeding steps within the INPROD process
    def _directories_(self, _scanDir, _outDir, _selection):

        #call global variables to change their values for this file
        self._global_outDir_(_outDir)
        self._global_scanDir_(_scanDir)
        self._global_selection_(_selection)

        directory = OUTSTR

        # Creates the images directory for new pdf to image conversions
        if not os.path.exists(directory + "/pdfs"):
            os.makedirs(directory + "/pdfs")

        # Creates the images directory for new pdf to image conversions
        if not os.path.exists(directory + "/images"):
            os.makedirs(directory + "/images")

        # Creates the text directory for OCR text files from each image
        if not os.path.exists(directory + "/text"):
            os.makedirs(directory + "/text")

        # Creates the completed directory for the concatenations of OCR text
        if not os.path.exists(directory + "/completed"):
            os.makedirs(directory + "/completed")

        #Chained Events
        self._duplicate_pdfs_()

    #Responsible for duplicating the PDF files to be operated on and ensure the integrity of the original files
    def _duplicate_pdfs_(self):

        scanDir = SCANSTR
        outDir = OUTSTR
        dstDir = (outDir + "/pdfs/")
        counter = 00

        #iterate over all files in directory
        for filename in os.listdir(scanDir):
            if filename.endswith(".pdf"):
                #counter for unique naming purposes
                counter += 1
                #name constructor* for the source file
                src_file = os.path.join(scanDir, filename)
                #the actual moving of the file
                shutil.copy((src_file), dstDir)

                #name constructor* for the destination file
                dst_file = os.path.join(dstDir, filename)
                #name constructor* for the new destination file
                new_dst_file = os.path.join(dstDir, str(counter) + ".pdf")
                os.rename(dst_file, new_dst_file)
        #Chained event
        self._pdf_to_img_()

    #Convert pdf to imges for further processing
    def _pdf_to_img_(self):
        # Set inital directory
        srcdir = SCANSTR
        outDir = OUTSTR
        directory = (outDir + "/pdfs/")



        # The function that determines what is and is not effected by this loop
        namingCounter = 0
        namingCounter = namingCounter + 1

        #iterate over files in named directory
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                #utilize wand to convert the pdfs into resolution 500 images and move them to a new directory with .jpg format
                pdf = wi(filename = directory + filename, resolution=500)
                corename = os.path.splitext(filename)[0]
                pdfImage = pdf.save(filename= outDir + "/images/" + corename + '.jpg')

        #chained event
        self._img_to_txt_()

    #Convert images to text files
    def _img_to_txt_(self):
        # The directory of the images
        directory = (OUTSTR + "/images/")
        txtDir = (OUTSTR + "/text/")
        c = 0

        # The directory file iteration loop",
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".tiff"):

                passFile = filename
                # Variable hold to
                hold = str(filename)
                # The function responsible for converting formats to jpeg sets resolution
                pdf = wi(filename= directory + hold, resolution=300)
                pdfImage = pdf.convert('jpeg')

                # Increment counter strictly for naming purposes
                c = c + 1

                # Sets array for image blobs taking in for OCR analysis
                imageBlobs = []

                for img in pdfImage.sequence:
                    imgPage = wi(image=img)
                    imageBlobs.append(imgPage.make_blob('jpeg'))

                # Individual OCR collections of the objects taken
                recognized_text = []

                for imgBlob in imageBlobs:
                    im = PIL.Image.open(io.BytesIO(imgBlob))
                    text = pytesseract.image_to_string(im, lang='eng')
                    recognized_text.append(text.encode('ascii', 'ignore'))

                # Visual check for the recognized text, DISABLE WHEN NOT TESTING
                # print(recognized_text)

                # Set a variable to the name of the file the loop is current operating with
                hold = filename

                # Use REGEX to only extract the name of the file and remove the subname-number
                # Very brute force and lazy way to do this fix when you have more time and focus!!!!!!
                r = re.compile(r'^[^.jpeg]*')
                nameCut = r.findall(hold)
                nameCut = str(nameCut)
                nameCut = nameCut.replace('[', '')
                nameCut = nameCut.replace(']', '')
                nameCut = nameCut.replace("'", '')
                finalCut = nameCut

                # Naming convention for file system
                with open(txtDir + finalCut + '.txt', 'w') as f:
                    print(recognized_text, file=f)



        #cahined event
        self._combine_txt_()

    #amalgamating text files together into one
    def _combine_txt_(self):

        directory = (OUTSTR + "/text/")
        compDir = (OUTSTR + "/completed/")
        counter = 0

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):

                # Set a variable to the name of the file the loop is current operating with
                firstLoop = filename

                # Use REGEX to only extract the name of the file and remove the sub-number
                a = re.compile(r'^[^-]*')
                mainNum = a.findall(firstLoop)

                b = re.compile('(?<=-)(.*\n?)(?=.txt)')
                subNum = b.findall(firstLoop)
                subNum = str(subNum)
                SubNum = re.sub(r"[^a-zA-Z0-9 ]+", "", subNum)

                hold = str(mainNum)
                finNum = re.sub(r"[^a-zA-Z0-9 ]+", "", hold)



                #The following is a stain on theis code file and apologize to anyone who has made it this far, this is
                #a brute force method to combine files of differing sizes from 1-7, due to time I was unable to write
                #a concise algorithm to do this and pass all tests, this will be removed prior to release
                if r'-' not in filename:
                    with open(directory + filename, 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                            file.write(raw0)

                elif SubNum == "1":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                file.write(raw0 + raw1)

                elif SubNum == "2":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(directory + (finNum + "-2.txt"), 'r') as myfile:
                                raw2 = myfile.read().replace(r'\n', '  ')
                                with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                    file.write(raw0 + raw1 + raw2)

                elif SubNum == "3":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(directory + (finNum + "-2.txt"), 'r') as myfile:
                                raw2 = myfile.read().replace(r'\n', '  ')
                                with open(directory + (finNum + "-3.txt"), 'r') as myfile:
                                    raw3 = myfile.read().replace(r'\n', '  ')
                                    with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                        file.write(raw0 + raw1 + raw2 + raw3)

                elif SubNum == "4":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(directory + (finNum + "-2.txt"), 'r') as myfile:
                                raw2 = myfile.read().replace(r'\n', '  ')
                                with open(directory + (finNum + "-3.txt"), 'r') as myfile:
                                    raw3 = myfile.read().replace(r'\n', '  ')
                                    with open(directory + (finNum + "-4.txt"), 'r') as myfile:
                                        raw4 = myfile.read().replace(r'\n', '  ')
                                        with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                            file.write(raw0 + raw1 + raw2 + raw3 + raw4)

                elif SubNum == "5":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(directory + (finNum + "-2.txt"), 'r') as myfile:
                                raw2 = myfile.read().replace(r'\n', '  ')
                                with open(directory + (finNum + "-3.txt"), 'r') as myfile:
                                    raw3 = myfile.read().replace(r'\n', '  ')
                                    with open(directory + (finNum + "-4.txt"), 'r') as myfile:
                                        raw4 = myfile.read().replace(r'\n', '  ')
                                        with open(directory + (finNum + "-5.txt"), 'r') as myfile:
                                            raw5 = myfile.read().replace(r'\n', '  ')
                                            with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                                file.write(raw0 + raw1 + raw2 + raw3 + raw5)

                elif SubNum == "6":
                    with open(directory + (finNum + "-0.txt"), 'r') as myfile:
                        raw0 = myfile.read().replace(r'\n', '  ')
                        with open(directory + (finNum + "-1.txt"), 'r') as myfile:
                            raw1 = myfile.read().replace(r'\n', '  ')
                            with open(directory + (finNum + "-2.txt"), 'r') as myfile:
                                raw2 = myfile.read().replace(r'\n', '  ')
                                with open(directory + (finNum + "-3.txt"), 'r') as myfile:
                                    raw3 = myfile.read().replace(r'\n', '  ')
                                    with open(directory + (finNum + "-4.txt"), 'r') as myfile:
                                        raw4 = myfile.read().replace(r'\n', '  ')
                                        with open(directory + (finNum + "-5.txt"), 'r') as myfile:
                                            raw5 = myfile.read().replace(r'\n', '  ')
                                            with open(directory + (finNum + "-6.txt"), 'r') as myfile:
                                                raw6 = myfile.read().replace(r'\n', '  ')
                                                with open(compDir + str(mainNum) + "-complete.txt", 'w') as file:
                                                    file.write(raw0 + raw1 + raw2 + raw3 + raw5 + raw6)


        #chained event
        self._clean_()


    #Responsible for cleaning the files to make them more readable for human recognition
    def _clean_(self):
        directory = (OUTSTR + "/completed/")

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                # Read in the file
                with open(directory + filename, 'r') as file:
                    filedata = file.read()

                # Removing formating pieces for OCR process
                # filedata = filedata.replace(r"\\n", ' ')
                filedata = filedata.replace(r"\n", '  ')
                filedata = filedata.replace(r"\'", '\'')
                filedata = filedata.replace(r"[b", ' ')
                filedata = filedata.replace(r"]", ' ')

                # Write the file out again
                with open(directory + filename, 'w') as file:
                    file.write(filedata)

        # Accuracy Check
        #tuner._accuracy_check_(directory)

        #Pass the global variables of scan and out directory to the first activated method of the Sort class
        Sorter._initalize_(SCANSTR, OUTSTR, SELECTION)
