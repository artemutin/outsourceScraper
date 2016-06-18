from bs4 import BeautifulSoup
from re import split
from datetime import date
from functools import partial

from sources.Page import BasePage


class GisDictionaryScraper:

    def __init__(self, page: str, city: str, region: int, scrape_details = False ):
        self.soup = BeautifulSoup(page, 'html.parser')
        self._ads = None
        self.scrape_details = scrape_details
        self._city = city
        self._region = region

    @property
    def ads(self):
        if self._ads is None:
            self.__read_ads()
            if self.scrape_details:
                self.__scrape_details()
        return self._ads

    def __read_ads(self)->None:
        self._ads = []
        for ad in self.soup.find_all("article", class_="miniCard"):
            d = dict()

            find = partial(search, ad)

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

            self._ads.append(d)

    def __scrape_details(self):
        for ad in self._ads:
            page = BasePage(ad['catalogURL'])
            soup = BeautifulSoup(page.page, 'html.parser')
            ad.update(catalogue_page_parse(soup))


def search(soup: BeautifulSoup, class_: str, elem='div'):
    return soup.find(elem, class_)


def tostr(s):
    return str(s).strip('\n\t\ ').replace(u'\xa0', u' ')