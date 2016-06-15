from bs4 import BeautifulSoup
from re import split,match
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
            #print(ad)
            d = dict()
            search = lambda cl: ad.find('div', class_=cl)
            info = search("company__info")
            d['firmTitle'] = str(info.header.h4.a.string).strip('\n\t')
            d['labeledCategory'] = str(info.find('div', class_="company__activity-type").string)

            info = search("company__side")
            d['renewDate'] = FarpostDictionaryScraper.__date_parse(info.div.string)

            info = search("company__details")
            d['firmShortDesc'] = str(info.div.string).strip('\n\t\ ')
            d['address'] = FarpostDictionaryScraper.__adress_parse(str(info.find('div', class_='contacts').div
                                                                       .get_text().strip('\n\t\ ')))

            self._ads.append(d)

    @classmethod
    def __date_parse(cls, datestr):
        s = split(r'\W+', datestr)
        return date(int(s[3]), 5, int(s[1]))

    @classmethod
    def __adress_parse(cls, address):
        print(address)
        s = split(r',', address)
        return {'region': 25, 'city': s[0], 'rest': ','.join(s[1:])}