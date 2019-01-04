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
    def _CRA_main_(self, passedFile, passedLoc):

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
        def hasNumbers(document):
            return any(char.isdigit() for char in document)

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



        # OLD - Should re-do this for a more neat better system
        #Variables declared so there is no errors if a flag is not tripped and a variable not set prior to csv print out
        AddressedTo = ""
        SIN = ""

        required_openclose = ""
        required_chequeSides = ""
        required_chequeSides_Amt = ""
        required_chequesCancelled = ""
        required_bankDrafts = ""
        required_certCheques = ""
        required_deposits = ""
        required_withdrawls = ""
        required_depositSlips = ""
        required_withdrawlSlips = ""
        required_creditMemo = ""
        required_debitMemo = ""
        required_transfersIn = ""
        required_transfersOut = ""
        required_wiresIn = ""
        required_wiresOut = ""
        required_liabilityApplications = ""
        required_liabilityStatements = ""
        required_mortgageApplications = ""
        required_mortgageStatements = ""
        required_loanApplications = ""
        required_loanStatements = ""
        required_CCStatements = ""
        required_CCApplications = ""
        required_CCApprovals = ""
        required_termDeposits = ""
        required_guaranteedInvestments = ""
        required_investmentAccounts = ""
        required_accountStatements = ""
        required_RRSP = ""
        required_RSP = ""
        required_RESP = ""
        required_TFSA = ""
        required_RRIF = ""
        required_GIC = ""
        statementAcc = ""
        sidesCheques = ""
        cancelledCheques = ""
        required_knowCustomer = ""
        required_corporateNum = ""
        required_safetyDeposit = ""
        required_sigCards = ""
        required_investments = ""
        required_mutualFunds = ""

        amt_chequeSides = ""
        amt_chequesCancelled = ""
        amt_bankDraft = ""
        amt_deposits = ""
        amt_certCheques = ""
        amt_withdrawls = ""
        amt_debitMemoAMT = ""
        amt_transfersInAMT = ""
        amt_transfersOutAMT = ""
        amt_wiresIn = ""
        amt_wiresOut = ""

        required_DOB = ""
        required_daysBetween = ""

        option_clientprofile = ""

        ####Customer Profile Details
        call_callFor = extract_callfor(string)
        call_acts = extract_acts(string)
        call_dateSent = extract_datesent(string)
        call_taxCenter = extract_taxcenter(string)
        call_taxCenter = [x[1] for x in call_taxCenter]
        call_requested = extract_requested(string)
        call_betweenDates = extract_between(string)
        now = datetime.datetime.now()
        call_currTime = now.strftime("%Y-%m-%d %H:%M")
        call_letterTitle = extract_letterTitle(string)
        call_letterTitle = [x[1] for x in call_letterTitle]
        call_requestingBody = extract_reqBody(string)

        ####Customer Request Details
        call_openCloseAcc = extract_var(string, "Opening and closing dates")
        call_accountsReq = extract_var(string, "accounts")
        call_chequeSides = extract_var(string, "cheques")
        call_chequesCancelled = extract_var(string, "cancelled cheques")
        call_certCheques = extract_var(string, "certified cheques")
        call_depositReq = extract_var(string, "all deposits")
        call_withdrawlsReq = extract_var(string, "all withdrawls")
        call_accounts = extract_var(string, "all accounts")
        call_transfersIn = extract_var(string, "transfers in")
        call_transfersOut = extract_var(string, "transfers out")
        call_wiresIn = extract_var(string, "wires in")
        call_wiresOut = extract_var(string, "wires out")
        call_CCStatements = extract_var(string, "credit card statement")
        call_CCApprovals = extract_var(string, "credit card approval")
        call_guaranteedInvestments =  extract_var(string, "guaranteed investments")
        call_investmentAccounts =  extract_var(string, "investment accounts")
        call_RRSP =  extract_var(string, "RRSP")
        call_RESP =  extract_var(string, "RESP")
        call_TFSA =  extract_var(string, "TFSA")
        call_knowCustomer = extract_var(string,"Know Your Customer")

        call_due = charThreshold(string, "days", 30, "date")
        call_chequeSidesAMT = charThreshold(string, "both sides of cheques", 50, "num")
        call_chequesCancelledAMT = charThreshold(string, "cancelled cheques", 50, "num")
        call_bankDraftAMT = charThreshold(string, "bank drafts", 50, "num")
        call_depositAMT = charThreshold(string, "all deposits", 50, "num")
        call_certChequesAMT = charThreshold(string, "certified cheques", 50, "num")
        call_withdrawlsAMT = charThreshold(string, "all withdrawls", 50, "num")
        call_debitMemoAMT = charThreshold(string, "debit memo", 50, "num")
        call_transfersInAMT = charThreshold(string, "transfers in", 50, "num")
        call_transfersOutAMT = charThreshold(string, "transfers out", 50, "num")
        call_wiresInAMT = charThreshold(string, "wires in", 50, "num")
        call_wiresOutAMT =  charThreshold(string, "wires out", 50, "num")

        #Determine if Client Profile needed
        option_clientprofile = extract_var(string, "client profile")
        if option_clientprofile == "Yes":
            required_deposits = "Yes"


        #↓↓↓↓↓↓↓↓To determine if the file is from Alberta and process its few certain differences↓↓↓↓↓↓↓↓#
        #Not a good system as Alberta can show up anywhere so find a better rule
        call_AddressedTo_param2 = extract_var_restricted(string, "Alberta",0,1500)
        call_AddressedTo_param3 = extract_var_restricted(string, "Debtor's name",0,1500)
        call_AddressedTo_param4 = extract_var_restricted(string, "Subject",0,1500)

        #If alberta identifer is caught do the following
        if call_AddressedTo_param2 == "Yes":
            AddressedTo = extract_search(string, "Name:", "Corporate", "Corporate Account")
            AddressedTo = str(AddressedTo)
            required_corporateNum = extract_search(string, "Number:", "By", "  ")
            required_corporateNum = str(required_corporateNum)


        elif call_AddressedTo_param3 == "Yes":
            AddressedTo = extract_search(string, "Debtor's name", "Other name", " ")
            AddressedTo = str(AddressedTo)
        elif call_AddressedTo_param4 == "Yes":
            AddressedTo = extract_search(string, "Subject", "SIN", " ")
            AddressedTo = str(AddressedTo)
        else:
            AddressedTo = str(extract_addressedto(string))
            required_corporateNum = "null"

        #↑↑↑↑↑↑↑↑To determine if the file is from Alberta and process its few certain differences↑↑↑↑↑↑↑↑#

        ##########---------- Date of Birth Starts ----------##########
        #Variables to search for
        call_DOB_param1 = extract_var(string, "DOB")
        call_DOB_param2 = extract_var(string, "date of birth")
        call_DOB_param3 = extract_var(string, "Birth Date of")
        call_DOB_param4 = extract_var(string, "D.O.B.")
        call_DOB_param5 = extract_var(string, "Birth:")
        if call_DOB_param1 == "Yes":
            required_DOB = retriveAll(string, "DOB", 23)
        if call_DOB_param2 == "Yes":
            required_DOB = retriveAll(string, "date of birth", 29)
        if call_DOB_param3 == "Yes":
            required_DOB = retriveAll(string, "Birth date of", 29)
        if call_DOB_param4 == "Yes":
            required_DOB = retriveAll(string, "D.O.B.", 26)
        if call_DOB_param5 == "Yes":
            required_DOB = retriveAll(string, "Birth:", 26)

        #cleaning extra characters and text from string
        required_DOB = ''.join(required_DOB)
        required_DOB = required_DOB.replace(",", "")
        required_DOB = required_DOB.replace("-", "")
        required_DOB = required_DOB.replace(".", "")
        required_DOB = required_DOB.replace(")", "")
        required_DOB = required_DOB.replace("(", "")
        required_DOB = required_DOB.replace(";", "")
        DOB_split = required_DOB.split(" ")

        #If the string contains any words not in the dateList arrau (days,months,years) remove them
        DOB_clean = [x for x in DOB_split if x in dateList]

        #join all the information in the array together with spaces
        DOB_clean_string = ' '.join(DOB_clean)

        #DOB final is equal to the joined array
        required_DOB = DOB_clean_string



        ##########---------- Days Between Starts ----------##########
        call_daysBetween_param1 = extract_var(string, "period")
        call_daysBetween_param2 = extract_var(string, "last 12 months")
        call_daysBetween_param3 = extract_var(string, "for the last")
        if call_daysBetween_param1 == "Yes":
            required_daysBetween = extract_search(string, "period", ":", "  ")
        elif call_daysBetween_param2 == "Yes":
            required_daysBetween = "last 12 months"
        elif call_daysBetween_param3 == "Yes":
            required_daysBetween = extract_search(string, "for the last", "months", "  ")

        ##########---------- GICs Starts ----------##########
        call_GIC_param1 = extract_var(string, "GIC")
        call_GIC_param2 = extract_var(string, "GICs")
        call_GIC_param3 = extract_var(string, "Guaranteed investment Certificates")

        if call_GIC_param1 == "Yes":
            required_GIC = "Yes"
        elif call_GIC_param2 == "Yes":
            required_GIC = "Yes"
        elif call_GIC_param3 == "Yes":
            required_GIC = "Yes"
        else:
            required_GIC = "No"

        ##########---------- Safety Deposit Starts ----------##########
        call_safetyDeposit_param1 = extract_var(string, "safety deposit")

        if call_safetyDeposit_param1 == "Yes":
            required_safetyDeposit = "Yes"
        else:
            required_safetyDeposit = "No"

        ##########---------- Signature Cards Starts ----------##########
        call_sigCards_param1 = extract_var(string, "signature authority cards")
        call_sigCards_param2 = extract_var(string, "signature cards")

        if call_sigCards_param1 == "Yes":
            required_sigCards = "Yes"
        elif call_sigCards_param2 == "Yes":
            required_sigCards = "Yes"
        else:
            required_sigCards = "No"

        ##########---------- RRIF Starts ----------##########
        call_RRIF_param1 = extract_var(string, "RRIF")
        call_RRIF_param2 = extract_var(string, "RRIFs")
        call_RRIF_param3 = extract_var(string, "(RRIF)")
        call_RRIF_param4 = extract_var(string, "registered retirement income fund")

        if call_RRIF_param1 == "Yes":
            required_RRIF = "Yes"
        elif call_RRIF_param2 == "Yes":
            required_RRIF = "Yes"
        elif call_RRIF_param3 == "Yes":
            required_RRIF = "Yes"
        elif call_RRIF_param4 == "Yes":
            required_RRIF = "Yes"
        else:
            required_RRIF = "No"

        ##########---------- RRSP Starts ----------##########
        call_RSP_param1 = extract_var(string, " RSP")
        call_RSP_param2 = extract_var(string, " RSPs")
        call_RSP_param3 = extract_var(string, ",RSP")
        call_RSP_param4 = extract_var(string, ",RSPs")
        call_RSP_param5 = extract_var(string, "(RSP)")
        call_RSP_param6 = extract_var(string, "retirement saving plans")
        call_RSP_param7 = extract_var(string, "retirement savings plan")

        if call_RSP_param1 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param2 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param3 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param4 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param5 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param6 == "Yes":
            required_RSP = "Yes"
        elif call_RSP_param7 == "Yes":
            required_RSP = "Yes"
        else:
            required_RSP = "No"

        ##########---------- Liability Applications Starts ----------##########
        call_liabilityApps_param1 = extract_var(string, "liability applications")
        call_liabilityApps_param2 = extract_var(string, "liability application")

        if call_liabilityApps_param1 == "Yes":
            required_liabilityApplications = "Yes"
        elif call_liabilityApps_param2 == "Yes":
            required_liabilityApplications = "Yes"
        else:
            required_liabilityApplications = "No"

        ##########---------- Liability Statement Starts ----------##########
        call_liabilityState_param1 = extract_var(string, "liability statements")
        call_liabilityState_param2 = extract_var(string, "liability statement")
        call_liabilityState_param3 = extract_var(string, "liabilities")


        if  call_liabilityState_param1 == "Yes":
            required_liabilityStatements = "Yes"
        elif  call_liabilityState_param2 == "Yes":
            required_liabilityStatements = "Yes"
        elif  call_liabilityState_param3 == "Yes":
            required_liabilityStatements = "Yes"
        else:
            required_liabilityStatements = "No"

        ##########---------- Investments Starts ----------##########
        call_investments_param1 = extract_var(string, "investments")
        call_investments_param2 = extract_var(string, "investment accounts")
        call_investments_param3 = extract_var(string, "investments statements")
        call_investments_param4 = extract_var(string, "bonds")
        call_investments_param5 = extract_var(string, "stocks")

        if call_investments_param1 == "Yes":
            required_investments = "Yes"
        elif call_investments_param2 == "Yes":
            required_investments = "Yes"
        elif call_investments_param3 == "Yes":
            required_investments = "Yes"
        elif call_investments_param4 == "Yes":
            required_investments = "Yes"
        elif call_investments_param5 == "Yes":
            required_investments = "Yes"
        else:
            required_investments = "No"

        ##########---------- Term Deposits Starts ----------##########
        call_termDeposits_param1 = extract_var(string, "term deposit")
        call_termDeposits_param2 = extract_var(string, "term deposits")

        if call_termDeposits_param1 == "Yes":
            required_termDeposits = "Yes"
        elif call_termDeposits_param2 == "Yes":
            required_termDeposits = "Yes"
        else:
            required_termDeposits = "No"

        ##########---------- Mutual Funds Starts ----------##########
        call_mutualFunds_param1 = extract_var(string, "mutual fund")
        call_mutualFunds_param2 = extract_var(string, "mutual funds")

        if call_mutualFunds_param1 == "Yes":
            required_mutualFunds = "Yes"
        elif call_mutualFunds_param2 == "Yes":
            required_mutualFunds = "Yes"
        else:
            required_mutualFunds = "No"

        ##########---------- Loan Statements Starts ----------##########
        call_loanStatement_param1 = extract_var(string, "loan statement")
        call_loanStatement_param2 = extract_var(string, "loan statements")

        if call_loanStatement_param1 == "Yes":
            required_loanStatements = "Yes"
        elif call_loanStatement_param2 == "Yes":
            required_loanStatements = "Yes"
        else:
            required_loanStatements = "No"

        ##########---------- Mortgage Statements Starts ----------##########
        call_mortgageStatement_param1 = extract_var(string, "mortgage statement")
        call_mortgageStatement_param2 = extract_var(string, "mortgage statements")
        call_mortgageStatement_param3 = extract_var(string, "mortgage")
        call_mortgageStatement_param4 = extract_var(string, "mortgages")

        if call_mortgageStatement_param1 == "Yes":
            required_mortgageStatements = "Yes"
        elif call_mortgageStatement_param2 == "Yes":
            required_mortgageStatements = "Yes"
        elif call_mortgageStatement_param3 == "Yes":
            required_mortgageStatements = "Yes"
        elif call_mortgageStatement_param4 == "Yes":
            required_mortgageStatements = "Yes"
        else:
            required_mortgageStatements = "No"

        ##########---------- Loan Applications Starts ----------##########
        call_loanApplications_param1 = extract_var(string, "loan application")
        call_loanApplications_param2 = extract_var(string, "loan applications")
        call_loanApplications_param3 = extract_var(string, "loan, mortgage and credit applications")
        call_loanApplications_param4 = extract_var(string, "loan, mortgage or credit applications")
        call_loanApplications_param5 = extract_var(string, "loan, mortgage applications")

        if call_loanApplications_param1 == "Yes":
            required_loanApplications = "Yes"
        elif call_loanApplications_param2 == "Yes":
            required_loanApplications = "Yes"
        elif call_loanApplications_param3 == "Yes":
            required_loanApplications = "Yes"
        elif call_loanApplications_param4 == "Yes":
            required_loanApplications = "Yes"
        elif call_loanApplications_param5 == "Yes":
            required_loanApplications = "Yes"
        else:
            required_loanApplications = "No"

        ##########---------- Mortgage Applications Starts ----------##########
        call_mortgageApplications_param1 = extract_var(string, "mortgage application")
        call_mortgageApplications_param2 = extract_var(string, "mortgage applications")
        call_mortgageApplications_param3 = extract_var(string, "loan, mortgage and credit applications")
        call_mortgageApplications_param4 = extract_var(string, "loan, mortgage or credit applications")
        call_mortgageApplications_param5 = extract_var(string, "loan, mortgage applications")

        if call_mortgageApplications_param1 == "Yes":
            required_mortgageApplications = "Yes"
        elif call_mortgageApplications_param2 == "Yes":
            required_mortgageApplications = "Yes"
        elif call_mortgageApplications_param3 == "Yes":
            required_mortgageApplications = "Yes"
        elif call_mortgageApplications_param4 == "Yes":
            required_mortgageApplications = "Yes"
        elif call_mortgageApplications_param5 == "Yes":
            required_mortgageApplications = "Yes"
        else:
            required_mortgageApplications = "No"

        ##########---------- Debit Memos Starts ----------##########
        # Complex catch statements
        call_debitMemo_param1 = extract_var(string, "debit memo")
        call_debitMemo_param2 = extract_var(string, "debit memos")

        if call_debitMemo_param1 == "Yes":
            required_debitMemo = "Yes"
        elif call_debitMemo_param2 == "Yes":
            required_debitMemo = "Yes"
        else:
            required_debitMemo = "No"

        ##########---------- Statement of accounts Starts ----------##########
        call_accountStatements_param1 = extract_var(string, "statements of account")
        call_accountStatements_param2 = extract_var(string, "statement of account")
        call_accountStatements_param3 = extract_var(string, "account statement")
        call_accountStatements_param4 = extract_var(string, "bank statements")

        if call_accountStatements_param1 == "Yes":
            required_accountStatements = "Yes"
        elif call_accountStatements_param2 == "Yes":
            required_accountStatements = "Yes"
        elif call_accountStatements_param3 == "Yes":
            required_accountStatements = "Yes"
        elif call_accountStatements_param4 == "Yes":
            required_accountStatements = "Yes"
        else:
            required_accountStatements = "No"

        ##########---------- Credit Applications Starts ----------##########
        call_CCApplications_param1 = extract_var(string, "credit application")
        call_CCApplications_param2 = extract_var(string, "credit applications")
        call_CCApplications_param3 = extract_var(string, "loan, mortgage and credit applications")
        call_CCApplications_param4 = extract_var(string, "loan, mortgage or credit applications")
        call_CCApplications_param5 = extract_var(string, "loan, mortgage applications")

        if call_CCApplications_param1 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param2 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param3 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param4 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param5 == "Yes":
            required_CCApplications = "Yes"
        else:
            required_CCApplications = "No"

        ##########---------- Bank Drafts Starts ----------##########
        call_bankDrafts_param1 = extract_var(string, "bank draft")
        call_bankDrafts_param2 = extract_var(string, "bank drafts")

        if call_bankDrafts_param1 == "Yes":
            required_bankDrafts = "Yes"
        elif call_bankDrafts_param2 == "Yes":
            required_bankDrafts = "Yes"
        else:
            required_bankDrafts = "No"

        ##########---------- Deposit Slips Starts ----------##########
        call_depositSlips_param1 = extract_var(string, "deposit slip")

        if call_depositSlips_param1 == "Yes":
            required_depositSlips = "Yes"
        else:
            required_depositSlips = "No"

        ##########---------- Withdrawl Slips Starts ----------##########
        call_withdrawlSlips_param1 = extract_var(string, "withdrawl slip")

        if call_withdrawlSlips_param1 == "Yes":
            required_withdrawlSlips = "Yes"
        else:
            required_withdrawlSlips = "No"

        ##########---------- Term Deposits Starts ----------##########
        call_creditMemo_param1 = extract_var(string, "credit memo")
        call_creditMemo_param2 = extract_var(string, "credit memos")

        if call_creditMemo_param1 == "Yes":
            required_creditMemo = "Yes"
        elif call_creditMemo_param2 == "Yes":
            required_creditMemo = "Yes"
        else:
            required_creditMemo = "No"


        ##########---------- SIN Starts ----------##########
        call_SIN_param1 = extract_var(string, "SIN ")
        call_SIN_param2 = extract_var(string, "SIN:")
        call_SIN_param3 = extract_var(string, "insurance number")
        call_SIN_param4 = extract_var(string, "SIN#")
        call_SIN_param5 = extract_var(string, "S.I.N.")
        call_SIN_param6 = extract_var(string, "insurance number:")

        #The following changes commonly found errors to improve accuracy
        if call_SIN_param1 == "Yes":
            SIN = retriveAll(string, "SIN ", 17)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SINfind)

        if call_SIN_param2 == "Yes":
            SIN = retriveAll(string, "SIN:", 18)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SINfind)
        if call_SIN_param3 == "Yes":
            SIN = retriveAll(string, "insurance number", 29)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SIN)
        if call_SIN_param4 == "Yes":
            SIN = retriveAll(string, "SIN#", 18)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SINfind)
        if call_SIN_param5 == "Yes":
            SIN = retriveAll(string, r"S.I.N.", 20)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SINfind)
        if call_SIN_param6 == "Yes":
            SIN = retriveAll(string, "insurance number:", 20)
            SIN = SIN.replace("o", "0")
            SIN = SIN.replace("O", "0")
            SIN = SIN.replace("l", "1")
            SIN = SIN.replace("L", "1")
            SIN = SIN.replace("(", "")
            SIN = SIN.replace(")", "")
            SINfind = extract_sin(SIN)
            SIN = SINfind
            print(SINfind)


        # Converting the necessary values to strings
        Filename = str(filename)
        Datesent = str(call_dateSent)
        Taxcenter = str(call_taxCenter)
        Due = str(call_due)
        Acts = str(call_acts)
        Requested = str(call_requested)
        Callfor = str(call_callFor)
        LOB = str(call_letterTitle)
        requestingBody = str(call_requestingBody)
        option_clientprofile = str(option_clientprofile)


        required_openclose = str(call_openCloseAcc)
        required_chequeSides = str(call_chequeSides)
        required_chequesCancelled = str(call_chequesCancelled)
        required_certCheques = str(call_certCheques)
        required_deposits = str(call_depositReq)
        required_withdrawls = str(call_withdrawlsReq)
        required_transfersIn = str(call_transfersIn)
        required_transfersOut = str(call_transfersOut)
        required_wiresIn = str(call_wiresIn)
        required_wiresOut = str(call_wiresOut)
        required_CCStatements = str(call_CCStatements)
        required_CCApprovals = str(call_CCApprovals)
        required_guaranteedInvestments = str(call_guaranteedInvestments)
        required_investmentAccounts = str(call_investmentAccounts)
        required_RRSP = str(call_RRSP)
        required_RESP = str(call_RESP)
        required_TFSA = str(call_TFSA)
        required_knowCustomer = str(call_knowCustomer)

        amt_chequeSides = str(call_chequeSidesAMT)
        amt_chequesCancelled = str(call_chequesCancelledAMT)
        amt_bankDraft = str(call_bankDraftAMT)
        amt_deposits = str(call_depositAMT)
        amt_certCheques = str(call_certChequesAMT)
        amt_withdrawls = str(call_withdrawlsAMT)
        amt_debitMemo = str(call_debitMemoAMT)
        amt_transfersIn = (call_transfersInAMT)
        amt_transferOut = (call_transfersOutAMT)
        amt_wiresIn = str(call_wiresInAMT)
        amt_wiresOut = str(call_wiresOutAMT)

        alberta_x_deposits = ""


        if call_AddressedTo_param2 == "Yes":
            alberta_number_deposits = extract_search(string, "last", "deposits", "into")
            if alberta_number_deposits is not None:
                alberta_num_flag = hasNumbers(str(alberta_number_deposits))
                if alberta_num_flag == True:
                    #alberta_number_deposits = re.sub("\D", "", str(alberta_number_deposits))
                    alberta_x_deposits = str(alberta_number_deposits)
                else:
                    alberta_x_deposits = str(alberta_number_deposits)

        amount_alberta_deposits = alberta_x_deposits

        if AddressedTo == "":
            AddressedTo == Callfor

        if  call_AddressedTo_param2 == "Yes":
            required_DOB = "null"

        #####Following is a sequence of string cleaning sequences

        # Cleaning the variables for display within the outputted file
        monthPat1 = r"January"
        monthPat2 = r"February"
        monthPat3 = r"March"
        monthPat4 = r"April"
        monthPat5 = r"May"
        monthPat6 = r"June"
        monthPat7 = r"July"
        monthPat8 = r"August"
        monthPat9 = r"September"
        monthPat10 = r"October"
        monthPat11 = r"November"
        monthPat12 = r"December"
        yearPat = r'|'.join(
            (monthPat1, monthPat2, monthPat3, monthPat4, monthPat5, monthPat6, monthPat7, monthPat8,
             monthPat9, monthPat10, monthPat11, monthPat12))

        # Formatting clearing
        forPat1 = r"\)\]"
        forPat2 = r"\[\("
        forPat3 = r"\'"
        forPat4 = r"\,"
        forPat5 = r"\]"
        forPat6 = r"\["
        forPat7 = r"\""
        fullForPat = r'|'.join((forPat1, forPat2, forPat3, forPat4, forPat5, forPat6, forPat7))

        # Date cleaning
        Datesent = re.sub(fullForPat, "", Datesent)

        # Tax Center Cleaning
        Taxcenter = re.sub(r"du Canada", "", Taxcenter)
        Taxcenter = re.sub(yearPat, "", Taxcenter)
        Taxcenter = re.sub(fullForPat, "", Taxcenter)
        Taxcenter = re.sub(' +', ' ', Taxcenter)

        # Name cleaning
        #Addressedto = re.sub(fullForPat, "", AddressedTo)

        # days due cleaning
        Due = re.sub(fullForPat, "", Due)
        Due = (Due + " days")

        # Acts cleaning
        Acts = re.sub(fullForPat, "", Acts)

        # Requested cleaning
        Requested = re.sub(fullForPat, "", Requested)
        Requested = re.sub("You", "", Requested)

        # SIN cleaning
        #SIN = re.sub(fullForPat, "", SIN)

        # CallTo cleaning
        Callfor = re.sub(fullForPat, "", Callfor)

        # LOB cleaning
        LOB = re.sub(fullForPat, "", LOB)
        sep = '  '
        LOB = LOB.split(sep, 2)[0]
        LOB = "TD " + LOB

        #AdressedTo Cleaning
        AddressedTo = str(AddressedTo)
        AddressedTo = re.sub(fullForPat, "", AddressedTo)
        AddressedTo = re.sub(":", "", AddressedTo)
        AddressedTo = re.sub("Name", "", AddressedTo)
        head,sep,tail = AddressedTo.partition('SIN')
        AddressedTo = head
        head, sep, tail = AddressedTo.partition('Corporate')
        AddressedTo = head
        head, sep, tail = AddressedTo.partition('DOB')
        AddressedTo = head
        head, sep, tail = AddressedTo.partition('Date')
        AddressedTo = head
        head, sep, tail = AddressedTo.partition('Social')
        AddressedTo = head
        hold = AddressedTo
        AddressedTo_cutParam1 = extract_var_pass(hold, "information on")
        if AddressedTo_cutParam1 == "Yes":
            head, sep, tail = AddressedTo.partition('information on')
            AddressedTo = tail
        else:
            AddressedTo = head

        #This is the current way that the variables are passed to an array to be printed into a csv
        # TO-DO : Please change amazingly inefficient
        var_list = [filename,
                    #LOB, Datesent,
                    call_currTime, AddressedTo,
                    SIN, required_corporateNum, required_DOB,
                    #Due,Taxcenter, Acts, Requested,Callfor, requestingBody,
                    option_clientprofile, required_knowCustomer, required_daysBetween,
                    required_openclose, required_accountStatements, required_chequeSides, amt_chequeSides,
                    required_chequesCancelled,amt_chequesCancelled, required_bankDrafts, amt_bankDraft, required_certCheques,amt_certCheques,
                    required_deposits, required_depositSlips, amt_deposits, required_withdrawls, required_withdrawlSlips, amt_withdrawls,"", required_creditMemo,
                    required_debitMemo,amt_debitMemo, required_transfersIn, amt_transfersIn, required_transfersOut, amt_transferOut,
                    required_wiresIn,amt_wiresIn, required_wiresOut, amt_wiresOut, required_liabilityApplications,
                    required_liabilityStatements,required_mortgageApplications,required_mortgageStatements,
                    required_loanApplications, required_loanStatements, required_CCApplications, required_CCStatements, required_CCApprovals,
                    required_termDeposits, required_investments, required_guaranteedInvestments, required_mutualFunds,
                    required_investmentAccounts, required_sigCards, required_safetyDeposit, required_GIC, required_RRIF, required_RRSP, required_RSP, required_RESP,required_TFSA,amount_alberta_deposits
                    ]
        #Create an instance of Collector in the Main.py
        collect = Collector()
        #Pass the var_list created to the english collector in Collect Main.py
        collect._english_collector(var_list, passedLoc)
