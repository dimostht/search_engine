import threading
import requests
from bs4 import BeautifulSoup
import urllib
import time
import os
import lxml.html


class Crawler:

    def __init__(self,url,limit,delete,threadsNumber,printBool = True):
        self.limit = limit
        self.url = url
        self.delete = delete
        self.threadsNumber = threadsNumber
        self.printBool = printBool
        self.titles = [ '' for _ in range(self.limit)]
        self.links = [ '' for _ in range(self.limit)]


        # if we have more threads than pages we use only the needed threads
        if self.limit < threadsNumber:
            self.threadsNumber = self.limit

    def getLimit(self):
        return self.limit

    def getTitles(self):
        return self.titles

    def getLinks(self):
        return self.links

    # get all the URLS in a webpage
    def getURLs(self,link):
        # get the URL's contents
        url_contents = urllib.parse.urlparse(link)
        reqs = requests.get(link)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        # all the links in this page
        links2 = []
        for l in soup.find_all('a'):
            if l is not None:
                links2.append(str(l.get('href')))

        # complete the links that don't have the correct start by using the contents of the main page
        links = []
        for l in links2:
            if l.startswith('/'):
                l = "http://"+url_contents[1]+l
            elif l.startswith('#'):
                l = 'http://' + url_contents[1] + url_contents[2] + l
            elif not l.startswith('http'):
                l = 'http://' + url_contents[1] + '/' + l
            links.append(l)

        return links

    # keep only text from a webpage
    def getText(self, link):
        html = urllib.request.urlopen(link)
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.findAll(text=True)
        title = soup.find('title')
        text = []
        for line in data:
            if not (line == '\n'):
                text.append(line)
        return title.string,text


    # crawl through the pages starting by the URL
    def crawl(self,name,link,i):
        # write all the text in the file
        # create the file to save the new page, the number is the number of
        # pages read in these crawler plus the pages read before, if the user wants to keep them
        fileNumber = i + self.data_count
        file = open("Data/page%d.txt" % fileNumber, 'w')

        try:
            title , text = self.getText(link)
            for t in text:
                file.write(t)
            file.close()
            self.titles[i] = title
            self.links[i] = link
            if self.printBool:
                print("Thread ",str(name+1)," readed ",title)
        except:
            file.close()
            self.titles[i] = "Link not accesible"
            self.links[i] = "Link not accesible"
            if self.printBool:
                print("Thread ", str(name + 1), " link not accesible ", link)

    def start(self):
        # delete its content depending of the variable
        path, dirs, files = next(os.walk("Data"))
        # the number of pages already saved in the folder
        self.data_count = len(files)
        # we delete them if the variable is True
        if self.delete == True:
            for i in range(self.data_count):
                os.remove("Data/page%i.txt" % i)
            self.data_count = 0
        # if we want to keep the previous files,
        # the variable data_count will add the new files read after these already saved

        self.allPages = []
        link = self.url
        self.allPages.append(link)

        # iterate through the links found till we reach the limit
        linksOfPage = []
        # starting by the first page, we get the URLs of each page
        pointer = 0
        while len(linksOfPage) < self.limit:
            linksOfPage = self.getURLs(self.allPages[pointer])
            pointer += 1

        # placing the new links at the end of the list
        for l in linksOfPage:
            self.allPages.append(l)

        linksReaded = 0

        # creating the threads
        threads = [None] * self.threadsNumber
        # calling each thread to crawl the next link will we reach the limit
        while linksReaded < self.limit:
            for i in range(self.threadsNumber):
                link = self.allPages[linksReaded]
                threads[i] = threading.Thread(target=self.crawl, args=(i,link,linksReaded))
                linksReaded+=1
                if linksReaded == self.limit:
                    self.threadsNumber = i+1
                    break
            # starting them
            for i in range(self.threadsNumber):
                threads[i].start()
            for i in range(self.threadsNumber):
                threads[i].join()

    def increment(self):
        global linksReaded
        linksReaded += 1




def main():
    """
    # starting url
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom"
    # bool variable to keep or delete previous data read
    delete = True
    # number of threads
    threadsNumber = 3

    t0 = time.time()
    # by calling the Crawler the threads start collecting data from the links
    c = Crawler(url,limit,delete,threadsNumber)
    c.start()
    print("Read ",limit," pages, using ",threadsNumber," threads in ",time.time()-t0," seconds.")
    """

if __name__ == "__main__":
    main()