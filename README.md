# search_engine


Crawler

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/WebCrawlerArchitecture.svg/1280px-WebCrawlerArchitecture.svg.png)

The Crawler gets the starting page and the limit of pages to crawl, it scans the pages of the pages and saves their content.
Crawler does not saves empty pages

Indexer

The Indexer calculates the TF (term frequency) and IDF (inverse document frequency) and creates the reversed catalogue of the pages.
Then it creates the cosine similarity betwean the pages.
Indexer also uses the Cleaner class to clean the content from special characters, empty space and stem words.

Query Processor

In the Query Processor the User enters the page to be compared and the number k of similar pages to receive.
Query Processor uses the Crawler and the Indexer to create a list of k pages most similar to the page the user gived.

