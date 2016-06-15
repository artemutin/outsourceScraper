from bs4 import BeautifulSoup

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
            self._ads.append(ad)

