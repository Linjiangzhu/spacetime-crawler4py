from threading import Thread

from utils.download import download
from utils import get_logger
from utils.textAnalyzer import TextAnalyzer
from collections import defaultdict
from scraper import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.requestedSiteCount = 0
        self.crawledSiteCount = 0
        self.crawledSiteSet = set()
        self.maxTextWordCount = 0
        self.maxTextWordCountPage = ""
        self.tokenDict =  defaultdict(int)
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                with open("word-token.txt", "a") as outfile:
                    for k, v in self.tokenDict.items():
                        outfile.write(f"{k} {v}\n")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}."
                f"\nsite requested: {self.requestedSiteCount}"
                f"\nsite crawled: {self.crawledSiteCount}"
                f"\nmax word count: {self.maxTextWordCount} site: {self.maxTextWordCountPage}"
            )
            scraped_urls = scraper(tbd_url, resp)
            self.requestedSiteCount += 1
            if 200 <= resp.status < 400:
                pageAnalyzer = TextAnalyzer(resp.raw_response.content)
                pageAnalyzer.execute()  
                self.crawledSiteCount += 1
                #pageText = pageTextExtract(resp.raw_response.content)
                #wc = wordCounter(pageText)
                wc = pageAnalyzer.getWordCount()
                pageAnalyzer.updateOldDict(self.tokenDict)
                monitor_word = self.tokenDict["and"]
                self.logger.info(
                    f"\nmonitor word 'and':{monitor_word}"
                )
                if wc > self.maxTextWordCount:
                    self.maxTextWordCount = wc
                    self.maxTextWordCountPage = resp.url
                
            self.crawledSiteSet.add(tbd_url)
            #print(f"site requested: {self.requestedSiteCount}\nsite crawled: {self.crawledSiteCount}")
            for scraped_url in scraped_urls:
                if scraped_url not in self.crawledSiteSet:
                    self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
