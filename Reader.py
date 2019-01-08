#####################DO NOT REMOVE###############################
##                                                             ##
##                DEVELOPED BY WAUN BRODERICK                  ##
##     PERSONAL BANKING - PERFORMANCE INTEGRITY OPERATIONS     ##
##                                                             ##
##                         08/208                              ##
##                                                             ##
##                RFI AUTOMATED INGESTION SYSTEM               ##
##                                                             ##
#####################DO NOT REMOVE###############################

from Main import *

import os.path
import re
from nltk.corpus import stopwords
import nltk
import datetime


class Parse:

    #Assigning global stop variable to the set of english stop words, eng is current use for dev line
    global stop
    stop = stopwords.words('english')

    #The method designed specifically for CRA & Alberta processing of documents
    def _function_bank_(self, passedFile, passedLoc):

        #Assigning imported variables
        filename = passedFile
        fileloc = passedLoc

        #Dictionary for number names to ints and back
        dict_numbers = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8,
                        'Nine' : 9, 'Ten' :  10, 'Eleven' : 11, 'Twelve' : 12, 'Thirteen' : 13,
                        'Fourteen' : 14, 'Fifteen' : 15, 'Sixteen' : 16, 'Seventeen' : 17, 'Eighteen' : 18,
                        'Nineteen': 19, 'Twenty' : 20, 'Twenty-One' : 21, 'Twenty-Two' : 22, 'Twenty-Three' : 23,
                        'Twenty-Four' : 24,'Twenty-Five' : 25 }

        #Dictionary for mapping months to values
        month_numbers = {'January': 1, 'February':2 , 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
                         'September':9, 'October':10, 'November':11, 'December':12}

        #Populate the list years with individual years between set numbers
        year = 1900
        years = []
        while year < 2100:
            years.append(year)
            year += 1

        #List of months and their abbreviations
        months = []
        months = ['January', 'Jan', 'February' , 'Feb', 'March', 'Mar', 'April', 'Apr', 'May', 'June', 'Jun', 'July', 'Jul',
                  'August', 'Aug', 'September', 'Sept', 'October', 'Oct', 'November', 'Nov', 'December', 'Dec']

        #List of Days populated of each day from 1 to the possible 31
        day = 0
        days = []
        while day < 31:
            days.append(day)
            day += 1

        #converting integers within list to string to match the text information
        days = list(map(str, days))
        years = list(map(str, years))

        #A combination of all the days months and year into the list dateList to be used for general purposes
        dateList = []
        dateList.extend(days)
        dateList.extend(months)
        dateList.extend(years)

        #List for words regarding amounts required
        amountTerms = ['over', 'under', 'excess', 'above', 'exceeding', '$', ',', '.', '0', '1', '2', '3', '4', '5','6',
                       '7', '8', '9', 0, 1, 2, 3, 4, 5, 6, 7 , 8 , 9, ]


        #To open each passed document and assign it to a string that can be manipulated
        with open(fileloc + filename, 'r+') as myfile:
            raw = myfile.read().replace(r'\n', '')
            wr = open(fileloc + filename, 'w')
            wr.write(raw)

            #string contains text document informaiton
            string = raw


        #Used if one desires to tokenize information from the document using nltk
        def ie_preprocess(document):
            document = ' '.join([i for i in document.split() if i not in stop])
            sentences = nltk.sent_tokenize(document)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]
            return sentences

        #OLD - A specific function used to extract specific addressed to information from doc
        def extract_addressedto(document):
            a = re.compile('(?<=Re:)(.*\n?)(?= To )')
            b = re.compile('(?<=Re:)(.*\n?)(?= For )')
            A = str(a.findall(string))
            B = str(b.findall(string))
            if (len(A) == 2):
                return b.findall(string)
            elif (len(B) == 2):
                return a.findall(string)
            elif (len(B) < len(A)):
                return b.findall(string)
            elif (len(A) < len(B)):
                return a.findall(string)
            else:
                return ("NOT FOUND")

        #OLD - A specific function used to extract specific call for to information from doc
        def extract_callfor(document):
            callfor = []
            r = re.compile('(?<= information for)(.*\n?)(?= Within )')
            return r.findall(string)

        #A regex sequence used to extract a SIN number on its specific digit content
        # TO-DO : Cand look for a following or starting char to ensure phone nums, etc. arent picked up
        def extract_sin(string):
            String = string
            r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3})')
            sin_numbers = r.findall(String)
            return [re.sub(r'\D', '', number) for number in sin_numbers]

        #OLD - A specific regex used to extract the date of birth when present in the dd-mm-yyyy or mm-dd-yyyy format
        def extract_dob(document):
            top = string[100:1500]
            r = re.compile(r'(\d{4}[-\.\s]??\d{2}[-\.\s]??\d{2}|\(\d{2}\)\s*\d{2}[-\.\s]??\d{4})')
            dob_numbers = r.findall(top)
            return [re.sub(r'\D', '', number) for number in dob_numbers]

        #OLD - A specific regex used to extract the acts being enforced
        def extract_acts(document):
            r = re.compile('(?<= enforce )(.*\n?)(?= we require )')
            return r.findall(string)

        #OLD - A specific regex used to extract the tax center
        def extract_taxcenter(document):
            top = string[0:200]
            r = re.compile(
                '(?:^|(?<= ))(du Canada)(.*\n?)(?:^|(?<= ))(January|February|March|April|May|June|July|August|September|October|November|December|REGISTERED)')
            return r.findall(top)
            return r.findall(string).group(1)

        #OLD - A specific regex used to extract the date it was being sent
        def extract_datesent(document):
            top = string[0:200]
            r = re.compile(
                '(?:^|(?<= ))(January|February|March|April|May|June|July|August|September|October|November|December)(.*\n?)(?:^|(?<= ))(2017|2018)')
            return r.findall(top)

        #OLD - A specific regex used to extract what is being requested
        def extract_requested(document):
            r = re.compile(
                '(?:^|(?<= ))(documents|documents:|names|person(s)|information/documents)(.*\n?)(?:^|(?<= ))(You|if you)')
            return r.findall(string)

        #OLD - A specific regex used to extract the date documents are requested between
        def extract_between(document):
            r = re.compile('(?<=period from)(.*\n?)(?=for all)')
            return r.findall(string)

        #OLD - A specific regex used to extract the title of the letter
        def extract_letterTitle(document):
            top = string[0:250]
            r = re.compile(
                '(?:^|(?<= ))(TD)(.*\n?)(?:^|(?<= ))(  )')
            return r.findall(top)
            return r.findall(string)

        #OLD - A specific search function to determine if it is from the canadian revenue agency
        def extract_reqBody(document):
            top = string[0:250]
            op1 = "Canada Revenue"
            out = ""
            r = re.search(op1, top)
            if r is not None:
                out = "Canada Revenue Agency"
            return(out)

        ################################################################################
        # Many of the previous methods are old and of varying degree of effectiveness  #
        #    The ones that follow are more generally encompassing and have been        #
        #               worked on following those stated previous.                     #
        ################################################################################


        #A method that accepts the string and searches for a word returning its presen with a Yes or No
        #THIS METHOD ALLOWS YOU TO PASS A STRING TO IT
        def extract_var_pass(document, find):
            lctx = find
            out = "No"
            r = re.search(lctx, document, re.IGNORECASE)
            if r is not None:
                out = "Yes"
            return(out)

        #A method that takes the document text and searches for a word returning its presen with a Yes or No
        #THIS METHOD WILL TAKE THE BASIC TEXT FROM THE WHOLE DOCUMENT
        def extract_var(document, find):
            lctx = find
            out = "No"
            r = re.search(lctx, string, re.IGNORECASE)
            if r is not None:
                out = "Yes"
            return(out)

        #A method that takes the document text, and a word, searches for the word within a character limit you can set on call
        def extract_var_restricted(document, find, start, stop):
            lctx = find
            out = "No"
            lowerLim = (start)
            upperLim = (stop)
            cutString = document[lowerLim:upperLim]
            r = re.search(lctx, cutString, re.IGNORECASE)
            if r is not None:
                out = "Yes"
            return (out)

        #Takes the document text and extracts the text between a starting word and stopping at any of 2 stop words
        def extract_search(document, start, end1, end2):
            r = re.compile(
                r"(?:^|(?<= ))(" + start + r")(.*\n?)(?:^|(?<= ))(" + end1 + r"|" + end2 + r")")
            return r.findall(string)

        #Search the document text for the first instance of a word then return the string with a threshold before and after
        def charThreshold(document, word, threshold, search):
            index = document.find(word)
            lowerLim = (index - threshold)
            upperLim = (index + threshold)
            cutString = document[lowerLim:upperLim]
            #print(cutString)
            if search == "num":
                cutString = cutString.replace(",", "")
                preList = re.findall(r'\b\d+\b', cutString)
                postList = [s for s in preList if len(s) >= 3]
                return (postList)
            elif search == "date":
                cutString = cutString.replace("(", "")
                cutString = cutString.replace(")", "")
                preList = re.findall(r'\b\d+\b', cutString)
                dueList = [s for s in preList if len(s) == 2]
                return (dueList)
            else:
                return(cutString)

        #Search the document text for the index of the first instance of a word then return the string with a threshold after
        def charAfter(document, word, threshold):
            index = document.find(word)
            thres = threshold
            upperLim = (index + thres)
            cutString = document[index:upperLim]
            return (cutString)

        #Allows you to pass a string to the file and set a top and bottom to segment the file with character indexing
        def segmentFile(document, top, bottom):
            string = document[top : bottom]
            return (str(string))

        #Allows you to pass a string and a created dictionary - UNFINISHED
        def dictFind(document, dictionary, find, option):
            string = document
            if find in dictionary:
                return dictionary[find]
            else:
                return("null")

        #returns if the string passed has any characters in it
        _digits = re.compile('\d')
        def containsDigits(string):
           return bool(_digits.search(string))




        #Pass a string and a word and return how many instances of the word the string contains
        def quantityFind(document, find):
            string = document
            r = re.findall(find, string, re.IGNORECASE)
            return (len(r))

        #Pass a string and a words, retrive all instances of the word with a set amount of characters following it
        def retriveAll(document, find, _following):
            string = document
            following = str(_following)
            allFinds = re.findall(find + r'.{' + following + r'}', string, re.IGNORECASE)
            listFinds = ', '.join(allFinds)
            #print(listFinds)
            return(listFinds)



        #This is the current way that the variables are passed to an array to be printed into a csv
        # TO-DO : Please change amazingly inefficient
        var_list = [
            #List of all variables created
                    ]
        #Create an instance of Collector in the Main.py
        collect = Collector()
        #Pass the var_list created to the english collector in Collect Main.py
        collect._english_collector(var_list, passedLoc)
