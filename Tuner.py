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

#import cv2
import os.path
#import math
#import numpy as np
#from scipy import ndimage
#import re
#import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#import sys

#Class responsible for pre Tuning files
#More complete version stored in other repository and will port later!
# NOT IMPLEMENTED SO NOT FULL TIED INTO PROGRAM WITH PROPER PASSING ETC

class Node(object):
    def __init__(self, name, threshold, location, run):
        self.name = name
        self.threshold = threshold
        self.location = location
        self.run = run
        self.next = None

class Queue(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.head == None

    def peek(self):
        obj = [ self.head.name, self.head.threshold, self.head.location, self.head.run ]
        return obj

    def peekPass(self):
        return self.head.run

    def peekThreshold(self):
        return self.head.threshold

    def enque(self, name, threshold, location, run):
        new_run = Node(name, threshold, location, run)
        if self.head is None:
            self.head = new_run
            self.tail = self.head
            self.size += 1
        else:
            self.tail.next = new_run
            self.tail = new_run
            self.size += 1

    def size(self):
        return self.size

    def dequeue(self):
        run = self.head.run
        self.head = self.head.next
        if self.head is None:
            self.tail is None
        return run

# class Tuning:
#     #skew correction method to correct for incorrect angles
#     def _skew_correction_(self):
#         # The directory of the images
#         directory = "./images/"
#         c = 0
#
#         # The directory file iteration loop",
#         for filename in os.listdir(directory):
#             if filename.endswith(".jpg"):
#
#                 img_before = cv2.imread(directory + filename)
#
#                 # cv2.imshow("Before", img_before)
#                 key = cv2.waitKey(0)
#
#                 img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
#                 img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
#                 lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
#
#                 angles = []
#
#                 for x1, y1, x2, y2 in lines[0]:
#                     cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
#                     angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
#                     angles.append(angle)
#
#                 median_angle = np.median(angles)
#                 img_rotated = ndimage.rotate(img_before, median_angle)
#
#                 print("Angle is {}".format(median_angle))
#                 cv2.imwrite(directory + 'rotated.jpg', img_rotated)
#                 # cv2.imshow("After", img_rotated)

class QC:

    def __init__(self):
        global firstQueue
        firstQueue = Queue()

    #Pipeline for rotating full pages
    # def _rotation_check_(self):
    #     directory = "./text/"
    #     emptyCount = 0
    #     stop_words_en = set(stopwords.words('english'))
    #     stop_words_fr = set(stopwords.words('french'))
    #
    #     for filename in os.listdir(directory):
    #         if filename.endswith(".txt"):
    #             with open(directory + filename, 'r') as myfile:
    #                 raw = myfile.read().replace(r'\n', '')
    #                 wr = open(directory + filename, 'w')
    #                 wr.write(raw)
    #
    #                 string = str(raw)
    #
    #                 #tokenization of works and filtering of sentences
    #                 word_tokens = word_tokenize(string)
    #                 filtered_sentence = [w for w in word_tokens if not w in stop_words_fr]
    #                 filtered_sentence = []
    #
    #                 for w in word_tokens:
    #                     if w not in stop_words_fr:
    #                         filtered_sentence.append(w)
    #
    #                         perCheck = int((len(filtered_sentence) / len(word_tokens)) * 100)
    #
    #                         # if perCount < 100:
    #                         #print(word_tokens)
    #                         print(filename)
    #                         print(perCheck)
    #                         if perCheck > 85:
    #                             print("hit")
    #                             cutName = str(filename)
    #                             a = re.compile(r'^[^-]*')
    #                             baseName = a.findall(cutName)
    #                             baseName = str(baseName)
    #                             BaseName = baseName.replace(".txt", "", 1)
    #                             finName = re.sub(r"[^a-zA-Z0-9 ]+", "", BaseName)
    #
    #                             b = re.compile('(?<=-)(.*\n?)(?=.txt)')
    #                             subName = b.findall(filename)
    #                             subName = str(subName)
    #                             SubName = re.sub(r"[^a-zA-Z0-9 ]+", "", subName)
    #
    #                             self._rotate_page_(finName, SubName)

    #indivudal call after identification to rotate the page
    #NOT IMPLEMENTED SO NOT FULL TIED INTO PROGRAM WITH PROPER PASSING ETC
    # def _rotate_page_(self,doc, page):
    #     directory = "./"
    #     targPDF = (doc + ".pdf")
    #     targPg = int(page)
    #     print(type(targPDF))
    #     print(type(targPg))
    #
    #     #
    #     actPDF = open(targPDF, 'rb')
    #     pdfReader = PyPDF2.PdfFileReader(actPDF)
    #     page = pdfReader.getPage(4)
    #     page.rotateClockwise(270)
    #
    #     pdfWriter = PyPDF2.PdfFileWriter()
    #     pdfWriter.addPage(page)
    #     resultPdfFile = open('rotatedPage.pdf', 'wb')
    #     pdfWriter.write(resultPdfFile)
    #     resultPdfFile.close()
    #     actPDF.close()
    #     sys.exit(0)

    def _accuracy_check_(self, _directory):
        stop_words_en = set(stopwords.words('english'))
        stop_words_fr = set(stopwords.words('french'))

        for filename in os.listdir(_directory):
            if filename.endswith(".txt"):
                # Read in the file
                with open(_directory + filename, 'r') as myfile:
                    raw = myfile.read().replace(r'\n', '')
                    wr = open(_directory + filename, 'w')
                    wr.write(raw)

                string = str(raw)

                # tokenization of works and filtering of sentences
                word_tokens = word_tokenize(string)
                filtered_sentence = [w for w in word_tokens if not w in stop_words_en]
                filtered_sentence = []

                for w in word_tokens:
                    if w not in stop_words_en:
                        filtered_sentence.append(w)

                        accuracyCheck = int((len(filtered_sentence) / len(word_tokens)) * 100)
                print ("this is the accuracy: " + str(accuracyCheck))
                if accuracyCheck <= 75:
                    firstQueue.enque(filename, accuracyCheck, _directory, 0)

        print("This is the legnth of the Queue: " + str(firstQueue.size))

    def _queue_loader_(self):
        print("This is the legnth of the Queue: " + firstQueue.qsize())


if __name__ == '__main__':
    # q.enque("file1", 20,"c:/documents/here", 1)
    # q.enque("file2", 56, "c:/documents/here", 2)
    # q.enque("file3", 77, "c:/documents/here", 2)
    # q.enque("file4", 34, "c:/documents/here", 2)
    # print (q.peekThreshold())
    # q.dequeue()
    # print(q.peekThreshold())
    # print(q.peek())
    # print("hello world")
    print("Hello World")
