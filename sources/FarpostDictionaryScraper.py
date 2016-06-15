from bs4 import BeautifulSoup
from re import split
from datetime import date

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
            search = lambda cl: ad.find('div', class_=cl)
            info = search("company__info")
            d['firmTitle'] = str(info.header.h4.a.string).strip('\n\t')
            d['labeledCategory'] = str(info.find('div', class_="company__activity-type").string)

            info = search("company__side")
            d['renewDate'] = FarpostDictionaryScraper.__date_convert(info.div.string)

            info = search("company__details")
            d['firmShortDesc'] = str(info.div.string).strip('\n\t\ ')

            self._ads.append(d)

    @classmethod
    def __date_convert(cls, datestr):
        s = split(r'\W+', datestr)
        return date(int(s[3]), 5, int(s[1]))