from bs4 import BeautifulSoup
from re import split,match
from datetime import date
from functools import partial
import urllib.request


class FarpostDictionaryScraper:

    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')
        self._ads = None

    @property
    def ads(self):
        if self._ads is None:
            self.__read_ads()

        return self._ads

    def __read_ads(self):
        self._ads = []
        for ad in self.soup.find_all("div", class_="company"):
            d = dict()
            find = partial(search, ad)

            info = find("company__info")
            d['firmTitle'] = tostr(info.header.h4.a.string)
            d['catalogURL'] = tostr(info.header.h4.a['href'])
            d['labeledCategory'] = tostr(find("company__activity-type").string)

            info = find("company__side")
            d['renewDate'] = date_parse(info.div.string)

            info = find("company__details")
            d['firmShortDesc'] = tostr(info.div.string)
            d['address'] = adress_parse(tostr(find('contacts').div.get_text()))

            self._ads.append(d)


def search(soup, class_):
    return soup.find('div', class_)


def tostr(s):
    return str(s).strip('\n\t\ ')


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
    d['phone'] = tostr(info.div.span.string)

    info = find("row contacts")
    d['email'] = tostr(search(info, 'email').a.string)
    d['site'] = tostr(search(info, 'website').a.string)

    return d
