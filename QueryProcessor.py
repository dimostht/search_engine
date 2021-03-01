import os
import sys
import time

import Indexer
import Crawler

class QueryProcessor():

    def findSimilar(self,link,limit):

        # we call the read text function from the Crawler to read the new link
        # we use the construcotr with empty variables
        crawler = Crawler.Crawler('',0,0,0)


        self.limit = limit
        file = open("Data/page%d.txt" % self.limit, 'w')

        try:
            self.title , text = crawler.getText(link)
            # we combine the lists of string to a single string
            text = ''.join(text)
            for t in text:
                file.write(t)
            file.close()
        except:
            "Link is not accesible"
            file.close()
            sys.exit(0)

        indexer = Indexer.Indexer()
        indexer.start()

        cosineSimilarity = indexer.getCosineSimilarity()



        linksId = [ i for i in range(self.limit)]

        linksIdSorted = [x for _,x in sorted(zip(cosineSimilarity,linksId),reverse=True)]

        return cosineSimilarity , linksIdSorted

    def getTitle(self):
        return self.title




def main():
    # starting url
    url = "https://en.wikipedia.org/wiki/London"
    # limit of pages
    limit = 10
    # bool variable to keep or delete previous data read
    delete = True
    # number of threads
    threadsNumber = 3



    t0 = time.time()
    # by calling the Crawler the threads start collecting data from the links
    crawler = Crawler.Crawler(url, limit, delete, threadsNumber,printBool=False)
    crawler.start()
    print("Read ", limit, " pages, using ", threadsNumber, " threads in ", time.time() - t0, " seconds.")

    queryProcessor = QueryProcessor()

    link = "https://en.wikipedia.org/wiki/Paris"

    # the k most similar links
    k = 4


    similarities , links = queryProcessor.findSimilar(link,limit)
    title = queryProcessor.getTitle()

    titles = crawler.getTitles()
    urls = crawler.getLinks()

    print()
    print(k," pages most similar to ",title)
    print()
    for i in range(k):
        x = links[i]
        print("With ",similarities[x]," similarity is",titles[x]," link: ",urls[x])

    print()
    print("Completed in ",time.time() -t0," seconds")

    # we delete the last page of the Data file,
    # this page is the page we just compared, by removing it
    # we can re-run the program with another page
    path, dirs, files = next(os.walk("Data"))
    last =  len(files) -1

    os.remove("Data/page%i.txt" % last)




if __name__ == "__main__":
    main()