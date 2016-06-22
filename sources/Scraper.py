import logging
from sources.Page import BasePage
from bs4 import BeautifulSoup
import concurrent.futures as Fut
from functools import partial


class Scraper:

    def __init__(self, page: BasePage, scrape_details=False, **kwargs):
        self.soup = BeautifulSoup(page.page, 'html.parser')
        self.scrape_details = scrape_details
        self.url = page.url
        self.load_ads()

    def load_ads(self):
        self.__read_ads()
        if self.scrape_details:
            self.__scrape_details()

    def all_ads(self):
        pass

    def scrape_ad(self, ad):
        pass

    def __read_ads(self)->None:
        self.ads = []
        logging.info('Started scraping detailed ads: url={}'.format(self.url))

        for ad in self.all_ads():
            scraped_ad = self.scrape_ad(ad)
            self.ads.append(scraped_ad)

        logging.info('Finished scraping ads: url={}'.format(self.url))

    def scrape_details_mapper(self, ad):
        pass

    def __scrape_details(self)->None:
        logging.info('Started scraping detailed ads: url={}'.format(self.url))
        with Fut.ThreadPoolExecutor(15) as executor:
            self.ads = executor.map(self.scrape_details_mapper, self.ads)

        logging.info('Finished scraping detailed ads: url={}'.format(self.url))


