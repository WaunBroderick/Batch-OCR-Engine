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

    global stop
    stop = stopwords.words('english')

    def _CRA_main_(self, passedFile, passedLoc):

        stop = stopwords.words('english')
        filename = passedFile
        fileloc = passedLoc

        dict_numbers = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8,
                        'Nine' : 9, 'Ten' :  10, 'Eleven' : 11, 'Twelve' : 12, 'Thirteen' : 13,
                        'Fourteen' : 14, 'Fifteen' : 15, 'Sixteen' : 16, 'Seventeen' : 17, 'Eighteen' : 18,
                        'Nineteen': 19, 'Twenty' : 20, 'Twenty-One' : 21, 'Twenty-Two' : 22, 'Twenty-Three' : 23,
                        'Twenty-Four' : 24,'Twenty-Five' : 25 }

        month_numbers = {'January': 1, 'February':2 , 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
                         'September':9, 'October':10, 'November':11, 'December':12}

        year = 1900
        years = []
        while year < 2100:
            years.append(year)
            year += 1

        months = []
        months = ['January', 'Jan', 'February' , 'Feb', 'March', 'Mar', 'April', 'Apr', 'May', 'June', 'Jun', 'July', 'Jul',
                  'August', 'Aug', 'September', 'Sept', 'October', 'Oct', 'November', 'Nov', 'December', 'Dec']

        day = 0
        days = []
        while day < 31:
            days.append(day)
            day += 1

        dateList = []
        days = list(map(str, days))
        years = list(map(str, years))

        dateList.extend(days)
        dateList.extend(months)
        dateList.extend(years)



        # Remove not registering formatting characters
        #print("file location: " + fileloc)
        #print("file name: " + filename)
        with open(fileloc + filename, 'r+') as myfile:
            raw = myfile.read().replace(r'\n', '')
            wr = open(fileloc + filename, 'w')
            wr.write(raw)

            string = raw
            #print(string)

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

        def extract_sin(string):
            String = string
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


        def extract_between(document):
            r = re.compile('(?<=period from)(.*\n?)(?=for all)')
            return r.findall(string)


        def extract_letterTitle(document):
            top = string[0:250]
            r = re.compile(
                '(?:^|(?<= ))(TD)(.*\n?)(?:^|(?<= ))(  )')
            return r.findall(top)
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

        def quantityFind(document, find):
            string = document
            r = re.findall(find, string, re.IGNORECASE)
            return (len(r))

        def retriveAll(document, find, _following):
            string = document
            following = str(_following)
            allFinds = re.findall(find + r'.{' + following + r'}', string, re.IGNORECASE)
            listFinds = ', '.join(allFinds)
            #print(listFinds)
            return(listFinds)




        #Variables
        AddressedTo = ""
        SIN = ""

        required_openclose = ""
        required_chequeSides = ""
        required_chequeSides_Amt = ""
        required_chequesCancelled = ""
        required_bankDraft = ""
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
        call_creditMemo = extract_var(string, "credit memoe")
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


        required_DOB = ''.join(required_DOB)
        required_DOB = required_DOB.replace(",", "")
        required_DOB = required_DOB.replace("-", "")
        required_DOB = required_DOB.replace(".", "")
        required_DOB = required_DOB.replace(")", "")
        required_DOB = required_DOB.replace("(", "")
        required_DOB = required_DOB.replace(";", "")
        DOB_split = required_DOB.split(" ")

        DOB_clean = [x for x in DOB_split if x in dateList]

        print("Before: ")
        print(DOB_split)
        print("After: ")
        print(DOB_clean)
        print("Days List: ")
        print(days)
        DOB_clean_string = ' '.join(DOB_clean)

        required_DOB = DOB_clean_string



        call_DOB_param1 = extract_var(string, "period")
        call_DOB_param2 = extract_var(string, "last 12 months")
        call_DOB_param3 = extract_var(string, "for the last")
        if call_DOB_param1 == "Yes":
            required_daysBetween = extract_search(string, "period", ":", "  ")
        elif call_DOB_param2 == "Yes":
            required_daysBetween = "last 12 months"
        elif call_DOB_param3 == "Yes":
            required_daysBetween = extract_search(string, "for the last", "months", "  ")



        ###############################GICS STARTS#############################################
        # Complex catch statements
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

        ###############################SAFETYDEPOSIT STARTS#############################################
        # Complex catch statements
        call_safetyDeposit_param1 = extract_var(string, "safety deposit")

        if call_safetyDeposit_param1 == "Yes":
            required_safetyDeposit = "Yes"
        else:
            required_safetyDeposit = "No"

        ###############################Signature Cards STARTS#############################################
        # Complex catch statements
        call_sigCards_param1 = extract_var(string, "signature authority cards")
        call_sigCards_param2 = extract_var(string, "signature cards")

        if call_sigCards_param1 == "Yes":
            required_sigCards = "Yes"
        elif call_sigCards_param2 == "Yes":
            required_sigCards = "Yes"
        else:
            required_sigCards = "No"

        ###############################RRIF STARTS#############################################
        # Complex catch statements
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

        ###############################RSP STARTS#############################################
        # Complex catch statements
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

        ###############################LIABILITY APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_liabilityApps_param1 = extract_var(string, "liability applications")
        call_liabilityApps_param2 = extract_var(string, "liability application")

        if call_RSP_param1 == "Yes":
            required_liabilityApplications = "Yes"
        elif call_RSP_param2 == "Yes":
            required_liabilityApplications = "Yes"
        else:
            required_liabilityApplications = "No"

        ###############################LIABILITY STATEMENSTS STARTS#############################################
        # Complex catch statements
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

        ###############################Investments STARTS#############################################
        # Complex catch statements
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

        ###############################Term Deposits APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_termDeposits_param1 = extract_var(string, "term deposit")
        call_termDeposits_param2 = extract_var(string, "term deposits")

        if call_termDeposits_param1 == "Yes":
            required_termDeposits = "Yes"
        elif call_termDeposits_param2 == "Yes":
            required_termDeposits = "Yes"
        else:
            required_termDeposits = "No"

        ###############################Mutual Funds APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_mutualFunds_param1 = extract_var(string, "mutual fund")
        call_mutualFunds_param2 = extract_var(string, "mutual funds")

        if call_mutualFunds_param1 == "Yes":
            required_mutualFunds = "Yes"
        elif call_mutualFunds_param2 == "Yes":
            required_mutualFunds = "Yes"
        else:
            required_mutualFunds = "No"

        ###############################Loan Statements APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_loanStatement_param1 = extract_var(string, "loan statement")
        call_loanStatement_param2 = extract_var(string, "loan statements")

        if call_loanStatement_param1 == "Yes":
            required_loanStatements = "Yes"
        elif call_loanStatement_param2 == "Yes":
            required_loanStatements = "Yes"
        else:
            required_loanStatements = "No"

        ###############################Mortgage Statements APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_mortgageStatement_param1 = extract_var(string, "mortgage statement")
        call_mortgageStatement_param2 = extract_var(string, "mortgage statements")

        if call_mortgageStatement_param1 == "Yes":
            required_mortgageStatements = "Yes"
        elif call_mortgageStatement_param2 == "Yes":
            required_mortgageStatements = "Yes"
        else:
            required_mortgageStatements = "No"

        ###############################Loan Statements APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_loanApplications_param1 = extract_var(string, "loan application")
        call_loanApplications_param2 = extract_var(string, "loan applications")

        if call_loanApplications_param1 == "Yes":
            required_loanApplications = "Yes"
        elif call_loanApplications_param2 == "Yes":
            required_loanApplications = "Yes"
        else:
            required_loanApplications = "No"

        ###############################Mortgage Statements APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_mortgageApplications_param1 = extract_var(string, "mortgage application")
        call_mortgageApplications_param2 = extract_var(string, "mortgage applications")

        if call_mortgageApplications_param1 == "Yes":
            required_mortgageApplications = "Yes"
        elif call_mortgageApplications_param2 == "Yes":
            required_mortgageApplications = "Yes"
        else:
            required_mortgageApplications = "No"

        ###############################Debit Memo APPLICATIONS STARTS#############################################
        # Complex catch statements
        call_debitMemo_param1 = extract_var(string, "debit memo")
        call_debitMemo_param2 = extract_var(string, "debit memos")

        if call_debitMemo_param1 == "Yes":
            required_debitMemo = "Yes"
        elif call_debitMemo_param2 == "Yes":
            required_debitMemo = "Yes"
        else:
            required_debitMemo = "No"

        ###############################Account Statements STARTS#############################################
        # Complex catch statements
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

        ###############################Credit Application STARTS#############################################
        # Complex catch statements
        call_CCApplications_param1 = extract_var(string, "credit applications")
        call_CCApplications_param2 = extract_var(string, "credit applications")

        if call_CCApplications_param1 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param2 == "Yes":
            required_CCApplications = "Yes"
        else:
            required_CCApplications = "No"

        ###############################Credit Application STARTS#############################################
        # Complex catch statements
        call_bankDrafts_param1 = extract_var(string, "bank draft")
        call_bankDrafts_param2 = extract_var(string, "bank drafts")

        if call_CCApplications_param1 == "Yes":
            required_CCApplications = "Yes"
        elif call_CCApplications_param2 == "Yes":
            required_CCApplications = "Yes"
        else:
            required_CCApplications = "No"


        ###############################Deposit Slips STARTS#############################################
        # Complex catch statements
        call_depositSlips_param1 = extract_var(string, "deposit slip")

        if call_depositSlips_param1 == "Yes":
            required_depositSlips = "Yes"
        else:
            required_depositSlips = "No"


        ###############################Withdrawl Slips STARTS#############################################
        # Complex catch statements
        call_withdrawlSlips_param1 = extract_var(string, "withdrawl slip")

        if call_withdrawlSlips_param1 == "Yes":
            required_withdrawlSlips = "Yes"
        else:
            required_withdrawlSlips = "No"




        # Converting the necessary values to strings
        Filename = str(filename)
        Datesent = str(call_dateSent)
        Taxcenter = str(call_taxCenter)
        Due = str(call_due)
        Acts = str(call_acts)
        Requested = str(call_requested)


        #hold until move confirmed valid
        call_SIN_param1 = extract_var(string, "SIN ")
        call_SIN_param2 = extract_var(string, "SIN:")
        call_SIN_param3 = extract_var(string, "insurance number")
        call_SIN_param4 = extract_var(string, "SIN#")
        call_SIN_param5 = extract_var(string, "S.I.N.")
        call_SIN_param6 = extract_var(string, "insurance number:")

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

        # numSum_SIN = 0
        # numSum_SIN = sum(x.isdigit() for x in SIN)
        # if numSum_SIN <4:
        #     SIN = "null"

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
        required_creditMemo = str(call_creditMemo)
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

        # #DOB Cleaning
        #required_DOB = str(required_DOB)
        # required_DOB = re.sub(fullForPat, "", required_DOB)
        # required_DOB = re.sub("birth", "", required_DOB)
        # required_DOB = re.sub("DOB", "", required_DOB)
        # required_DOB = re.sub("D.O.B.", "", required_DOB)
        # required_DOB = re.sub("date", "", required_DOB)
        # required_DOB = re.sub("of", "", required_DOB)
        # required_DOB = re.sub(":", "", required_DOB)
        # required_DOB = re.sub("is", "", required_DOB)
        # required_DOB = re.sub(";", "", required_DOB)
        # required_DOB = re.sub("social", "", required_DOB)

        # sep = 'SIN'
        # required_DOB = re.split(sep, required_DOB, flags=re.IGNORECASE)[0]
        #
        # sep2 = 'Dear'
        # required_DOB = re.split(sep2, required_DOB, flags=re.IGNORECASE)[0]
        #
        # sep3 = 'and'
        # required_DOB = re.split(sep3, required_DOB, flags=re.IGNORECASE)[0]
        #
        # sep4 = 'within'
        # required_DOB = re.split(sep4, required_DOB, flags=re.IGNORECASE)[0]
        #
        # sep5 = 'in'
        # required_DOB = re.split(sep5, required_DOB, flags=re.IGNORECASE)[0]
        #
        # sep6 = 'all'
        # required_DOB = re.split(sep6, required_DOB, flags=re.IGNORECASE)[0]
        #
        #
        # required_DOB = re.split(r"\)", required_DOB, flags=re.IGNORECASE)[0]

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
                    required_openclose, required_accountStatements, required_chequeSides, amt_chequeSides,
                    required_chequesCancelled,amt_chequesCancelled,amt_bankDraft, required_certCheques,amt_certCheques,
                    required_deposits, required_depositSlips, amt_deposits, required_withdrawls, required_withdrawlSlips, amt_withdrawls,"", required_creditMemo,
                    required_debitMemo,amt_debitMemo, required_transfersIn, amt_transfersIn, required_transfersOut, amt_transferOut,
                    required_wiresIn,amt_wiresIn, required_wiresOut, amt_wiresOut, required_liabilityApplications,
                    required_liabilityStatements,required_mortgageApplications,required_mortgageStatements,
                    required_loanApplications, required_loanStatements, required_CCApplications, required_CCStatements, required_CCApprovals,
                    required_termDeposits, required_investments, required_guaranteedInvestments, required_mutualFunds,
                    required_investmentAccounts, required_sigCards, required_safetyDeposit, required_GIC, required_RRIF, required_RRSP, required_RSP, required_RESP,required_TFSA,amount_alberta_deposits
                    ]
        #print(var_list)
        collect = Collector()
        collect._english_collector(var_list, passedLoc)
