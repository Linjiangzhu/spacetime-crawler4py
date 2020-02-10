from threading import Thread

from utils.download import download
from utils import get_logger
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
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}."
                f"\nsite requested: {self.requestedSiteCount}"
                f"\nsite crawled: {self.crawledSiteCount}"
            )
            scraped_urls = scraper(tbd_url, resp)
            self.requestedSiteCount += 1
            if 200 <= resp.status < 400:
                self.crawledSiteCount += 1
            self.crawledSiteSet.add(tbd_url)
            #print(f"site requested: {self.requestedSiteCount}\nsite crawled: {self.crawledSiteCount}")
            for scraped_url in scraped_urls:
                if scraped_url not in self.crawledSiteSet:
                    self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
