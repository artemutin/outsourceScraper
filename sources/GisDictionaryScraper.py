from bs4 import BeautifulSoup
from typing import List
from re import split
from functools import partial
from math import ceil
from urllib.request import unquote
import logging
import concurrent.futures as Fut

from sources.Page import BasePage
from sources.utils import cities


class CatalogPage(BasePage):
    pass


class GisDictionaryScraper:

    def __init__(self, page: CatalogPage, city: str, region: int, scrape_details = False ):
        self.soup = BeautifulSoup(page.page, 'html.parser')
        self._ads = get_empty_dictlist()
        self.scrape_details = scrape_details
        self._city = city
        self._region = region
        self._url = page.url

    @property
    def ads(self)->List[dict]:
        if self._ads is None:
            self.__read_ads()
            if self.scrape_details:
                self.__scrape_details()
        return self._ads

    def __read_ads(self)->None:
        self._ads = []
        logging.info('Started scraping ads: url={}'.format(self._url))
        for ad in self.soup.find_all("article", class_="miniCard"):
            try:
                d = dict()

                info = search(ad, "miniCard__headerTitle", 'h3')
                d['firmTitle'] = tostr(info.a.string)
                d['catalogURL'] = tostr(info.a['href'])
                d['renewDate'] = None
                d['labeledCategory'] = None

                d['renewDate'] = None

                info = search(ad, "miniCard__micro")
                if info:
                    d['firmShortDesc'] = tostr(info.string)
                else:
                    d['firmShortDesc'] = ''
                info = search(ad, "miniCard__address", 'span')
                d['address'] = {'region': self._region, 'city': self._city, 'rest': tostr(info.string) }

                if ad.find('div', attrs = {'data-adv': 'реклама'}):
                    d['promoted'] = True

                self._ads.append(d)
            except Exception as e:
                logging.error('Scraping of url={} failed with {}'.format( self._url, str(e)) )

        logging.info('Finished scraping ads: url={}'.format(self._url))

    def __scrape_details(self)->None:
        logging.info('Started scraping detailed ads: url={}'.format(self._url))
        with Fut.ThreadPoolExecutor(3) as executor:
            try:
                self._ads = executor.map(scrape_details_mapper, self._ads, timeout=15)
            except Exception as e:
                logging.error("Error in concurrent scrape: {}".format(str(e)))

        logging.info('Finished scraping detailed ads: url={}'.format(self._url))


def scrape_details_mapper(ad: dict)->dict:
    try:
        page = BasePage(ad['catalogURL'])
        soup = BeautifulSoup(page.page, 'html.parser')
        if ad.get('promoted', False):
            page = BasePage(soup.find('a', class_='firmCard__adsText')['href'])
            soup = BeautifulSoup(page.page, 'html.parser')
            ad['firmAdvertisement'] = soup.find('div', class_='articleCard__content').get_text()

        ad.update(catalogue_page_parse(soup))
        return ad
    except Exception as e:
        logging.error('Scraping of details for url={} failed with {}'.format(ad['catalogURL'], str(e)))


def search(soup: BeautifulSoup, class_: str, elem='div'):
    return soup.find(elem, class_)


def tostr(s):
    return str(s).strip('\n\t\ ').replace(u'\xa0', u' ')


def toint(s):
    if s:
        return int(s)
    else:
        return None


def catalogue_page_parse(page_soup):
    d = dict()
    try:
        d['phone'] = tostr(page_soup.find('a', class_='contact__phonesItemLink').span.string)
    except Exception:
        d['phone'] = ''

    d['email'] = ''
    try:
        d['site'] = tostr(page_soup.find('a', class_='link contact__linkText')['href'])
    except Exception:
        d['site'] = ''

    return d


def get_empty_dictlist()->List[dict]:
    return None


class CatalogPage(BasePage):
    def __init__(self, url, request = None, is_url_page = False):
        if request:
            url += '{}/'.format(request)

        if not is_url_page:
            super().__init__(url)
            self.url = unquote(split(r'\?', url)[0]) + '/'
            # get name of the city
            city = split(r'/', url)[3]
            self.city = ''
            for (ru, en) in cities.items():
                if en == city:
                    self.city = ru
                    break
        else:
            self.page = url
            self.url = None

        self._bs = BeautifulSoup(self.page, 'html.parser')
        firm_num = split(' ',
                            self._bs.find('h1', class_='searchResults__headerName').text
                         )[0]

        num = toint(firm_num)
        if num:
            self.num_pages = ceil(num/12)
        else:
            self.num_pages = 1

        self.page_num = int(self._bs.find('span', class_='pagination__page _current').string)

    def go_next(self):
        if self.num_pages > self.page_num:
            self.__init__('https://2gis.ru' +
                          self._bs.find('span', class_='pagination__page _current').next_sibling['href'])
            return self
        else:
            return None
