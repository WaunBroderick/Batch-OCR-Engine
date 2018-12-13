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

from Main import *

import os.path
import re
from nltk.corpus import stopwords
import nltk
import datetime


class Parse:

    def _CRA_main_(self, passedFile, passedLoc):

        stop = stopwords.words('english')
        filename = passedFile
        fileloc = passedLoc

        dict_numbers = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8,
                        'Nine' : 9, 'Ten' :  10, 'Eleven' : 11, 'Twelve' : 12, 'Thirteen' : 13,
                        'Fourteen' : 14, 'Fifteen' : 15, 'Sixteen' : 16, 'Seventeen' : 17, 'Eighteen' : 18,
                        'Nineteen': 19, 'Twenty' : 20, 'Twenty-One' : 21, 'Twenty-Two' : 22, 'Twenty-Three' : 23,
                        'Twenty-Four' : 24,'Twenty-Five' : 25 }

        # Remove not registering formatting characters
        print("file location: " + fileloc)
        print("file name: " + filename)
        with open(fileloc + filename, 'r+') as myfile:
            raw = myfile.read().replace(r'\n', '')
            wr = open(fileloc + filename, 'w')
            wr.write(raw)

            string = raw
            print(string)

        def ie_preprocess(document):
            document = ' '.join([i for i in document.split() if i not in stop])
            sentences = nltk.sent_tokenize(document)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]
            return sentences


        def extract_addressedto(document):
            addressedto = []
            # r = re.compile('Re:(.{10})')
            a = re.compile('(?<=Re:)(.*\n?)(?= To )')
            b = re.compile('(?<=Re:)(.*\n?)(?= For )')
            A = str(a.findall(string))
            B = str(b.findall(string))
            # print("a: " + A + "len: " + str(len(A)))
            # print("b: " + B + "len: " + str(len(B)))
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

        def extract_callfor(document):
            callfor = []
            r = re.compile('(?<= information for)(.*\n?)(?= Within )')
            return r.findall(string)

        def extract_sin(document, string):
            String = string
            # r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]??\d{3})')
            r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3})')
            sin_numbers = r.findall(String)
            return [re.sub(r'\D', '', number) for number in sin_numbers]

        def extract_dob(document):
            top = string[100:1500]
            r = re.compile(r'(\d{4}[-\.\s]??\d{2}[-\.\s]??\d{2}|\(\d{2}\)\s*\d{2}[-\.\s]??\d{4})')
            dob_numbers = r.findall(top)
            return [re.sub(r'\D', '', number) for number in dob_numbers]

        def extract_acts(document):
            acts = []
            r = re.compile('(?<= enforce )(.*\n?)(?= we require )')
            return r.findall(string)

        def extract_taxcenter(document):
            top = string[0:200]
            r = re.compile(
                '(?:^|(?<= ))(du Canada)(.*\n?)(?:^|(?<= ))(January|February|March|April|May|June|July|August|September|October|November|December|REGISTERED)')
            return r.findall(top)
            return r.findall(string).group(1)

        def extract_datesent(document):
            datesent = []
            top = string[0:200]
            r = re.compile(
                '(?:^|(?<= ))(January|February|March|April|May|June|July|August|September|October|November|December)(.*\n?)(?:^|(?<= ))(2017|2018)')
            return r.findall(top)

        def extract_requested(document):
            requested = []
            r = re.compile(
                '(?:^|(?<= ))(documents|documents:|names|person(s)|information/documents)(.*\n?)(?:^|(?<= ))(You|if you)')
            return r.findall(string)

        def extract_LOB(document):
            r = re.compile('(?:^|(?<= ))(TD)(.*\n?)(?:^|(?<= ))(  )')
            return r.findall(string)

        def extract_between(document):
            r = re.compile('(?<=period from)(.*\n?)(?=for all)')
            return r.findall(string)


        def extract_letterTitle(document):
            top = string[0:250]
            r = re.compile(
                '(?:^|(?<= ))(TD)(.*\n?)(?:^|(?<= ))(  )')
            return r.findall(top)
            return r.findall(string)

        def extract_due(document):
            due = []
            sentences = ie_preprocess(document)
            for tagged_sentence in sentences:
                for chunk in nltk.ne_chunk(tagged_sentence):
                    r = re.compile('(?<=Within)(.*\n?)(?= days of )')
                    return r.findall(string)

        def extract_period(document):
            due = []
            sentences = ie_preprocess(document)
            for tagged_sentence in sentences:
                for chunk in nltk.ne_chunk(tagged_sentence):
                    r = re.compile('(?<=Within )(.*\n?)(?= days of )')
                    return r.findall(string)

        def extract_reqBody(document):
            top = string[0:250]
            op1 = "Canada Revenue"
            out = ""
            r = re.search(op1, top)
            if r is not None:
                out = "Canada Revenue Agency"
            return(out)


        def extract_var_pass(document, docType):
            lctx = docType
            out = "No"
            r = re.search(lctx, document, re.IGNORECASE)
            if r is not None:
                out = "Yes"
            return(out)


        def extract_var(document, find):
            lctx = find
            out = "No"
            r = re.search(lctx, string, re.IGNORECASE)
            if r is not None:
                out = "Yes"
            return(out)

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

        def extract_search(document, start, end1, end2):
            r = re.compile(
                r"(?:^|(?<= ))(" + start + r")(.*\n?)(?:^|(?<= ))(" + end1 + r"|" + end2 + r")")
            return r.findall(string)

        def charThreshold(document, word, threshold, search):
            index = document.find(word)
            thres = threshold
            lowerLim = (index - threshold)
            upperLim = (index + threshold)
            cutString = document[lowerLim:upperLim]
            print(cutString)
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

        def charAfter(document, word, threshold):
            index = document.find(word)
            thres = threshold
            upperLim = (index + thres)
            cutString = document[index:upperLim]
            return (cutString)

        def segmentFile(document, _top, _bottom):
            string = document[_top : _bottom]
            return (str(string))

        def dictFind(document, dictionary, find, option):
            string = document
            if find in dictionary:
                return dictionary[find]
            else:
                return("null")

        def hasNumbers(document):
            return any(char.isdigit() for char in document)



        #Variables
        AddressedTo = ""
        SIN = ""

        required_openclose = ""
        required_accounts = ""
        required_chequeSides = ""
        required_chequeSides_Amt = ""
        required_chequesCancelled = ""
        required_bankDraft = ""
        required_certCheques = ""
        required_deposits = ""
        required_withdrawls = ""
        required_creditMemo = ""
        required_accounts = ""
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
        required_CCApprovals = ""
        required_termDeposits = ""
        required_guaranteedInvestments = ""
        required_mutualFunds = ""
        required_investmentAccounts = ""
        required_RRSP = ""
        required_RSP = ""
        required_RESP = ""
        required_TFSA = ""
        required_RRIF = ""
        statementAcc = ""
        sidesCheques = ""
        cancelledCheques = ""
        required_knowCustomer = ""
        required_corporateNum = ""

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
        call_chequeSides = extract_var(string, "both sides of cheques")
        call_chequesCancelled = extract_var(string, "cancelled cheques")
        call_bankDrafts = extract_var(string, "bank drafts")
        call_certCheques = extract_var(string, "certified cheques")
        call_depositReq = extract_var(string, "all deposits")
        call_withdrawlsReq = extract_var(string, "all withdrawls")
        call_creditMemo = extract_var(string, "credit memoe")
        call_accounts = extract_var(string, "all accounts")
        call_debitMemo = extract_var(string, "debit memo")
        call_transfersIn = extract_var(string, "transfers in")
        call_transfersOut = extract_var(string, "transfers out")
        call_wiresIn = extract_var(string, "wires in")
        call_wiresOut = extract_var(string, "wires out")
        call_liabilityApplications = extract_var(string, "liability application")
        call_liabilityStatements = extract_var(string, "liability statement")
        call_mortgageApplications = extract_var(string, "mortgage application")
        call_mortgageStatements = extract_var(string, "mortgage statement")
        call_loanApplications = extract_var(string, "loan applications")
        call_loanStatements = extract_var(string, "loan statement")
        call_CCStatements = extract_var(string, "credit card statement")
        call_CCApprovals = extract_var(string, "credit card approval")
        call_termDeposits =  extract_var(string, "term deposit")
        call_guaranteedInvestments =  extract_var(string, "guaranteed investments")
        call_mutualFunds =  extract_var(string, "mutual funds")
        call_investmentAccounts =  extract_var(string, "investment accounts")
        call_RRSP =  extract_var(string, "RRSP")
        call_RSP =  extract_var(string, "RSP")
        call_RESP =  extract_var(string, "RESP")
        call_TFSA =  extract_var(string, "TFSA")
        call_RRIF = extract_var(string, "RRIF")
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

        option_clientprofile = extract_var(string, "client profile")
        if option_clientprofile == "Yes":
            required_deposits = "Yes"


        #Complex catch statements
        call_AddressedTo_param2 = extract_var_restricted(string, "Alberta",0,1500)
        call_AddressedTo_param3 = extract_var_restricted(string, "Debtor's name",0,1500)
        call_AddressedTo_param4 = extract_var_restricted(string, "Subject",0,1500)


        if call_AddressedTo_param2 == "Yes":
            AddressedTo = extract_search(string, "Name:", "Corporate", "Corporate Account")
            AddressedTo = str(AddressedTo)
            required_corporateNum = extract_search(string, "Number:", "By", "  ")
            required_corporateNum = str(required_corporateNum)

        # else:
        #     AddressedTo = str(extract_addressedto(string))
        elif call_AddressedTo_param3 == "Yes":
            AddressedTo = extract_search(string, "Debtor's name", "Other name", " ")
            AddressedTo = str(AddressedTo)
        elif call_AddressedTo_param4 == "Yes":
            AddressedTo = extract_search(string, "Subject", "SIN", " ")
            AddressedTo = str(AddressedTo)
        else:
            AddressedTo = str(extract_addressedto(string))
            required_corporateNum = "null"



        call_DOB_param1 = extract_var(string, "DOB")
        call_DOB_param2 = extract_var(string, "birth")
        if call_DOB_param1 == "Yes":
            required_DOB = extract_search(string, "DOB", "Address", "  ")
        elif call_DOB_param2 == "Yes":
            required_DOB = extract_search(string, "birth", "Social", "  ")
        else:
            required_DOB = ""

        call_DOB_param1 = extract_var(string, "period")
        call_DOB_param2 = extract_var(string, "last 12 months")
        call_DOB_param3 = extract_var(string, "for the last")
        if call_DOB_param1 == "Yes":
            required_daysBetween = extract_search(string, "period", ":", "  ")
        elif call_DOB_param2 == "Yes":
            required_daysBetween = "last 12 months"
        elif call_DOB_param3 == "Yes":
            required_daysBetween = extract_search(string, "for the last", "months", "  ")





        # Converting the necessary values to strings
        Filename = str(filename)
        Datesent = str(call_dateSent)
        Taxcenter = str(call_taxCenter)
        Due = str(call_due)
        Acts = str(call_acts)
        Requested = str(call_requested)


        #hold until move confirmed valid
        call_SIN_param1 = extract_var(string, "SIN")
        call_SIN_param2 = extract_var(string, "insurance number")
        if call_SIN_param1 == "Yes":
            SIN = str(charAfter(string, "SIN", 25))
            SIN = str(extract_sin(string, SIN))
        elif call_SIN_param2 == "Yes":
            SIN = str(charAfter(string, "number", 10))
            SIN = str(extract_sin(string, SIN))
        if call_AddressedTo_param2 == "Yes":
            SIN = "null"

        Callfor = str(call_callFor)
        LOB = str(call_letterTitle)
        requestingBody = str(call_requestingBody)

        option_clientprofile = str(option_clientprofile)


        required_openclose = str(call_openCloseAcc)
        required_accounts = str(call_accountsReq)
        required_chequeSides = str(call_chequeSides)
        required_chequesCancelled = str(call_chequesCancelled)
        required_bankDrafts = str(call_bankDrafts)
        required_certCheques = str(call_certCheques)
        required_deposits = str(call_depositReq)
        required_withdrawls = str(call_withdrawlsReq)
        required_creditMemo = str(call_creditMemo)
        required_debitMemo = str(call_debitMemo)
        required_accounts = str(call_accounts)
        required_transfersIn = str(call_transfersIn)
        required_transfersOut = str(call_transfersOut)
        required_wiresIn = str(call_wiresIn)
        required_wiresOut = str(call_wiresOut)
        required_liabilityApplications = str(call_liabilityApplications)
        required_liabilityStatements =  str(call_liabilityStatements)
        required_mortgageApplications = str(call_mortgageApplications)
        required_mortgageStatements = str(call_mortgageStatements)
        required_loanApplications = str(call_loanApplications)
        required_loanStatements = str (call_loanStatements)
        required_CCStatements = str(call_CCStatements)
        required_CCApprovals = str(call_CCApprovals)
        required_termDeposits = str(call_termDeposits)
        required_guaranteedInvestments = str(call_guaranteedInvestments)
        required_mutualFunds = str(call_mutualFunds)
        required_investmentAccounts = str(call_investmentAccounts)
        required_RRSP = str(call_RRSP)
        required_RSP = str(call_RSP)
        required_RESP = str(call_RESP)
        required_TFSA = str(call_TFSA)
        required_RRIF = str(call_RRIF)
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
        SIN = re.sub(fullForPat, "", SIN)

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

        var_list = [filename,
                    #LOB, Datesent,
                    call_currTime, AddressedTo,
                    SIN, required_corporateNum, required_DOB,
                    #Due,Taxcenter, Acts, Requested,Callfor, requestingBody,
                    option_clientprofile, required_knowCustomer, required_daysBetween,
                    required_openclose, required_accounts, required_chequeSides, amt_chequeSides,
                    required_chequesCancelled,amt_chequesCancelled,required_bankDrafts,amt_bankDraft, required_certCheques,amt_certCheques,
                    required_deposits,amt_deposits, required_withdrawls,amt_withdrawls,"", required_creditMemo,
                    required_debitMemo,amt_debitMemo, required_transfersIn, amt_transfersIn, required_transfersOut, amt_transferOut,
                    required_wiresIn,amt_wiresIn, required_wiresOut, amt_wiresOut, required_liabilityApplications,
                    required_liabilityStatements,required_mortgageApplications,required_mortgageStatements,
                    required_loanApplications, required_loanStatements, required_CCStatements, required_CCApprovals,
                    required_termDeposits, required_guaranteedInvestments, required_mutualFunds,
                    required_investmentAccounts, required_RRSP, required_RSP, required_RESP,required_TFSA,amount_alberta_deposits
                    ]
        print(var_list)
        collect = Collector()
        collect._english_collector(var_list, passedLoc)
