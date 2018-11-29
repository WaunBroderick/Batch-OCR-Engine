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

from Reader import *

import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import os.path
import shutil
from threading import Thread
import sys


class Sort:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')


    def _global_scanDir_(self, _scanDir):
        global SCANSTR
        SCANSTR = _scanDir


    def _global_outDir_(self, _outDir):
        global OUTSTR
        OUTSTR = _outDir

    # Global defined variable for the selection
    def _global_selection_(self, _selection):
        global SELECTION
        SELECTION = _selection

    def _initalize_(self, _scanDir, _outDir, _selection):
        self._global_outDir_(_outDir)
        self._global_scanDir_(_scanDir)
        self._global_selection_(_selection)
        self._determine_language_()

    def _calculate_languages_ratios_(text):
        languages_ratios = {}

        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]

        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)

            languages_ratios[language] = len(common_elements)  # language "score"

            #A testing printline to output the variation of language detected in a document
            #print("Language Ratios: " + languages_ratios)

        return languages_ratios

    def _detect_language_(text):
        ratios = Sort._calculate_languages_ratios_(text)

        most_rated_language = max(ratios, key=ratios.get)

        return most_rated_language

    def _determine_language_(text):

        # Sets the directory for the traversed completed files to be operated on
        directory = (OUTSTR + "/completed/")
        print(OUTSTR)
        print(SCANSTR)
        languages_ratios = {}

        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".txt"):
                # Remove not registering formatting characters
                with open(directory + filename, 'r+') as myfile:
                    raw = myfile.read().replace(r'\n', '')
                    wr = open(directory + filename, 'w')
                    wr.write(raw)

                    string = str(raw)
                    text = string

                    language = Sort._detect_language_(text)

                    # A testing printline to output the final language detected in a document
                    #print(language)
                    # Creates the images directory for new language specific text
                    # if not os.path.exists(directory + language):
                    #     os.makedirs(directory + language)

                    movdir = (directory + language + "/")
                    # print(movdir)
                    # shutil.copy(directory + filename, movdir + filename)
                    # #os.remove(directory + filename)

                    src = (directory + filename)
                    dst = (movdir + filename)

                    Thread(target=shutil.copy, args=[src, dst]).start()


    def _english_subSorter_(self):
        # Sets the sub-directories for the traversed completed files to be operated on
        parse = Parse()

        directory = (OUTSTR + "/completed/")

        headers = ["filename", "Letter Title", "date sent", "date recieved",
                   "Customer Name", "Social Insurance Number", "Date Of Birth",
                   "Date Due", "Tax Center", "Subsections", "Raw Information",
                   "Information For", "Agency","//Client Profile", "//Know your customer", "//Days Between", "Opening and Closing of Accounts","Statements of Account", "Both sides of Cheques",
                   "//AMT PLACE HOLDER", "Cancelled Cheques","AMT PLACE HOLDER", "Bank Drafts",
                   "//AMT PLACE HOLDER","Certified Cheques","//AMT PLACE HOLDER", "//Deposits","//AMT PLACE HOLDER",
                   "Withdrawls","//AMT PLACE HOLDER","Last # deposits", "Credit Memos","Debit Memos",
                   "//AMT PLACE HOLDER", "Transfers into Acc","//AMT PLACE HOLDER","Transfers out of Account", "//AMT PLACE HOLDER",
                   "Wires into Acc","//AMT PLACE HOLDER", "Wires out of Acc", "//AMT PLACE HOLDER",
                   "Liability Applications", "Liability Statements", "Mortgage Applications", "Mortgage Statements",
                   "Loan Applications", "Loan Statements", "Credit Card Statements", "Credit Card Approvals",
                   "Term Deposits", "Guaranteed Investments", "Mutual Funds", "investment Acounts", "RRSP", "RSP",
                   "RESP", "TFSA",
                    ]
        with open(directory + '/eng-final.csv', 'a') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(headers)

        for filename in os.listdir(directory):
            if SELECTION == "RFI":
                parse._CRA_main_(filename, directory)
            elif SELECTION == "Audit":
                messagebox.showinfo("Process Selection", "Audit is not implemented yet, please restart and try a different process")
                sys.exit()
            elif SELECTION == "RESL":
                messagebox.showinfo("Process Selection", "RESL is not implemented yet, please restart and try a different process")
                sys.exit()
            else:
                messagebox.showinfo("Process Selection", "THERE HAS BEEN AN ERRRORRRR")
                sys.exit()

    def _french_subSorter_(self):
        # Sets the sub-directories for the traversed completed files to be operated on
        parse = Parse()

        directory = (OUTSTR + "/completed/french/")
        fileLoc = (directory)
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                fileLoc = (directory + filename)
                #parse._FR_main_(filename, directory)
