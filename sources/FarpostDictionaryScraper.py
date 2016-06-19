from bs4 import BeautifulSoup
from re import split
from datetime import date
from functools import partial
import requests
import logging

from sources.Page import BasePage


class CatalogPage(BasePage):
    pass


class FarpostDictionaryScraper:

    def __init__(self, page: CatalogPage, scrape_details = False, **kwargs):
        self.soup = BeautifulSoup(page.page, 'html.parser')
        self._ads = None
        self.scrape_details = scrape_details
        self._url = page.url

    @property
    def ads(self):
        if self._ads is None:
            self.__read_ads()
            if self.scrape_details:
                self.__scrape_details()
        return self._ads


    def __read_ads(self)->None:
        self._ads = []
        logging.info('Started scraping detailed ads: url={}'.format(self._url))
        for ad in self.soup.find_all("div", class_="company"):
            try:
                d = dict()
                find = partial(search, ad)

                info = find("company__info")
                if not info:
                    logging.warning('Could not find company info')
                d['firmTitle'] = tostr(info.header.h4.a.string)
                d['catalogURL'] = tostr(info.header.h4.a['href'])
                act_type = find("company__activity-type")
                if act_type:
                    d['labeledCategory'] = tostr(act_type.string)

                info = find("company__side")
                d['renewDate'] = date_parse(info.div.string)

                info = find("company__details")
                if info.div:
                    d['firmShortDesc'] = tostr(info.div.string)
                d['address'] = adress_parse(tostr(find('contacts').div.get_text()))

                self._ads.append(d)
            except Exception as e:
                logging.error('Scraping of url={} failed with {}'.format(self._url, str(e)))

        logging.info('Finished scraping ads: url={}'.format(self._url))

    def __scrape_details(self):
        logging.info('Started scraping detailed ads: url={}'.format(self._url))
        for ad in self._ads:
            try:
                page = BasePage(ad['catalogURL'])
                soup = BeautifulSoup(page.page, 'html.parser')
                ad.update(catalogue_page_parse(soup))
            except Exception as e:
                logging.error('Scraping of details for url={} failed with {}'.format(ad['catalogURL'], str(e)) )

        logging.info('Finished scraping detailed ads: url={}'.format(self._url))


def search(soup: BeautifulSoup, class_: str):
    return soup.find('div', class_)


def tostr(s):
    return str(s).strip('\n\t\ ')


def toint(s):
    if s:
        return int(s)
    else:
        return None


def date_parse(datestr):
    s = split(r'\W+', datestr)
    months = {'января': 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6, "июля": 7, "августа": 8,
              "сентября": 9, "ноября": 10, "октября": 11, "декабря": 12}
    return date(int(s[3]), months.get(s[2]), int(s[1]))


def adress_parse(address):
    s = split(r',', address)
    return {'region': 25, 'city': s[0], 'rest': ','.join(s[1:])}


def catalogue_page_parse(page_soup):
    d = dict()
    find = partial(search, page_soup)
    info = find("address-phones")
    try:
        d['phone'] = tostr(info.div.span.string)
    except AttributeError:
        d['phone'] = ''

    info = find("row contacts")
    try:
        d['email'] = tostr(search(info, 'email').a.string)
    except AttributeError:
        d['email'] = ''
    try:
        d['site'] = tostr(search(info, 'website').a.string)
    except AttributeError:
        d['site'] = ''

    return d


FULL_CATALOG_URL = 'http://www.vl.ru/main/0/'


class CatalogPage(BasePage):
    def __init__(self, url, request = None, is_url_page = False):
        if request:
            url += '?search={}'.format(request)

        if not is_url_page:
            super().__init__(url, cookies={'city': '0'})
        else:
            self.page = url
            self.url = None

        self._bs = BeautifulSoup(self.page, 'html.parser')
        num = self._bs.find('a', id='link-last')
        if num:
            self.num_pages = int(num.text)
            # this happens only if pager has many links and ...
        else:
            last_li = self._bs.find('ul', class_='pager-list').find_all('li')[-1]
            if last_li.a:
                s = last_li.a.string
            else:
                s = last_li.string
            num = toint(s)
            if num:
                self.num_pages = num
            else:
                self.num_pages = 1

        self.page_num = int(self._bs.find('li', class_='current').text)

    def go_next(self):
        if self.num_pages > self.page_num:
            self.__init__(self._bs.find('li', class_='current').next_sibling.a['href'])
            return self
        else:
            return None