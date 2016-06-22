from bs4 import BeautifulSoup
from typing import List
from re import split
from math import ceil
from urllib.request import unquote
import logging
from re import match, sub

from sources.Page import BasePage
from sources.utils import cities
from sources.Scraper import Scraper, tostr, toint, search


class CatalogPage(BasePage):
    pass


class GisDictionaryScraper(Scraper):

    def __init__(self, page: CatalogPage, city: str, region: int, scrape_details = False ):
        self._city = city
        self._region = region
        super().__init__(page, scrape_details, num_threads=3)

    def all_ads(self):
        return self.soup.find_all("article", class_="miniCard")

    def scrape_ad(self, ad):
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

            if ad.find('div', attrs={'data-adv': 'реклама'}):
                d['promoted'] = True

            return d
        except Exception as e:
            logging.error('Scraping of url={} failed with {}'.format(self.url, str(e)) )
            return None

    def scrape_details_mapper(self, ad: dict) -> dict:
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
        if match(r'http://link\.2gis.*',  d['site']):
            d['site'] = match(r'.*\?(.*)', d['site']).group(1)
    except Exception:
        d['site'] = ''

    return d


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
