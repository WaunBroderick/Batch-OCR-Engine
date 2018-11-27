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


import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

    def peekName(self):
        return self.head.name

    def peekLocation(self):
        return self.head.location

    def enque(self, name, threshold, location, run):
        new_node = Node(name, threshold, location, run)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
            self.size += 1
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    def size(self):
        return self.size

    def dequeue(self):
        run = self.head.run
        self.head = self.head.next
        if self.head is None:
            self.tail is None
        return run

class QC:

    #def __init__(self):


    def _accuracy_check_(self, _directory):
        firstQueue = Queue()
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
                    print(filename)
                    print(_directory)
                    print(accuracyCheck)
                    firstQueue.enque(filename, accuracyCheck, _directory, 0)

        print("This is the legnth of the Queue: " + str(firstQueue.size))
        print("This is the threshold in the head of the Queue: " + str(firstQueue.peekThreshold()))
        print("This is the name in the head of the Queue: " + str(firstQueue.peekName()))
        print("This is the location in the head of the Queue: " + str(firstQueue.peekLocation()))
        #print("This is the location in the head of the Queue: " + str(firstQueue.peekLocation))

        #self._queue_loader_()

    # def _queue_loader_(self):
    #     runLoops = firstQueue.size
    #     fileName = str(firstQueue.peekName)
    #     fileName = fileName.replace("complete.txt", "", 1)
    #     fileName = fileName.replace("']", "", 1)
    #     fileName = fileName.replace("['", "", 1)
    #     print("this is the fileName: " + fileName)



# if __name__ == '__main__':
#     q = Queue()
#     q.enque("file1", 20,"c:/documents/here", 1)
#     q.enque("file2", 56, "c:/documents/here", 2)
#     q.enque("file3", 77, "c:/documents/here", 2)
#     q.enque("file4", 34, "c:/documents/here", 2)
#     print (q.peekThreshold())
#     q.dequeue()
#     print(q.peekThreshold())
#     print(q.peek())
#     print("hello world")
#     print("Hello World")
