import re
import string
import time
import numpy as np
from bs4 import BeautifulSoup
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy import spatial


# a class to clean the text data from the pages
class Cleaner:

    # remove html
    def remove_html(self, text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    # remove numbers
    def remove_numbers(self,text):
        result = re.sub(r'\d+', ' ', text)
        return result

    # remove punctuation
    def remove_punctuation(self,text):
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        return text.translate(translator)

    # remove whitespace but no new lines
    def remove_whitespace(self,text):
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.strip(' ')
        text.replace('\n','')
        return text

    def clean(self,text):
        text = self.remove_html(text)
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.remove_whitespace(text)
        return text.lower()


    # a class to create the reversed index


class Indexer:

    def start(self):
        # create a cleaner
        cleaner = Cleaner()

        # get the number of pages we have in the Data file
        path, dirs, files = next(os.walk("Data"))
        # the number of pages saved in the folder
        count = len(files)

        files = [None] * count

        # save the cleaned text in the files array
        for i in range(count):
            files[i] = cleaner.clean(open('Data/page%i.txt' % i, 'r').read())


        tokensPerPage2 = [[None] for _ in range(count)]

        # all the words of a page
        for i in range(count):
            tokensPerPage2[i] = files[i].split(' ')

        # stem the tokens
        ps = PorterStemmer()
        stop_words = set(stopwords.words('english'))

        tokensPerPage =  [[] for _ in range(count)]

        for i in range(count):
            for w in tokensPerPage2[i]:
                if not (w in stop_words):
                    word = ps.stem(w)
                    if word != None:
                        tokensPerPage[i].append(word)



        allTokens = []
        for t in tokensPerPage:
            for w in t:
                allTokens.append(w)

        # tokens has no duplicates
        tokens = list(dict.fromkeys(allTokens))
        """
        # the reversed catalogue dictionary
        self.reversedCatalogue = dict()


        # for the each file check for every token
        for i in range(count):
            file = files[i]
            for word in tokens :
                # check if the word is in this specific file
                if word in file:
                    # if the word is not at the catalogue we add a array at its slot
                    if word not in self.reversedCatalogue:
                        self.reversedCatalogue[word] = []
                    # if the word already exist in the catalogue we add the number
                    # of the file at its array
                    if word in self.reversedCatalogue:
                        self.reversedCatalogue[word].append(i)
        """

        self.tf_idf = {}

        for word in tokens:
            df = 0
            for i in range(count):
                # we use the tokensPerPage variable to take into account the stemmed words
                tf = 0
                if len(tokensPerPage[i])>0:
                    tf = tokensPerPage[i].count(word) / len(tokensPerPage[i])
                if word in tokensPerPage[i]:
                    df += 1
                # log of the total number of pages devided by the number of pages that have the word
                idf = np.log(count / (df + 1))
                self.tf_idf[i,word] = tf * idf

        tfidf2 = [[] for _ in range(count)]

        for i, w in self.tf_idf:
            tfidf2[i].append(self.tf_idf[i, w])

        # a array with the cosine similarity of each page to the last one
        self.cosineSimilarity = []

        # the last page is the one we want to compare to the others
        for i in range(count-1):
                result = 1 - spatial.distance.cosine(tfidf2[i], tfidf2[count-1])
                self.cosineSimilarity.append(result)

    def getReversedIndex(self):
        return self.reversedCatalogue

    def getTFIDF(self):
        return self.tf_idf

    def getCosineSimilarity(self):
        return self.cosineSimilarity


def main():
    """
    t0 = time.time()

    indexer = Indexer()
    indexer.start()

    catalogue = indexer.getReversedIndex()
    tfidf = indexer.getTFIDF()
    cosineSimilarity = indexer.getCosineSimilarity()

    print(cosineSimilarity)

    print()
    t1 = time.time() - t0
    print("Completed in ",t1," seconds")
    """



if __name__ == "__main__":
    main()
























