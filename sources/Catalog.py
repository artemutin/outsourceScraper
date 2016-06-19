import sources.FarpostDictionaryScraper as F
import sources.GisDictionaryScraper as G
from logging import info
from typing import List
from sources.utils import catalogs, cities


def scrape_catalog(catalog: str, category: str, city: str)->List[dict]:
    if catalog == 'vl':
        pages = map(F.CatalogPage, catalogs.get(catalog).get(category))
        Sc = F.FarpostDictionaryScraper
    elif catalog == '2gis':
        pages = map(lambda cat: G.CatalogPage('https://2gis.ru/{city}/{category}'.format(city=cities.get(city),
                                                                      category=cat)), catalogs.get(catalog).get(category))
        Sc = G.GisDictionaryScraper

    ads = []
    i = 1
    for page in pages:
        while True:
            info('parsing page {}'.format(i))
            scraper = Sc(page, city=city, region=27)
            # print(page.page)
            ads.extend(scraper.ads)
            i += 1
            page = page.go_next()
            if not page: break

    return ads


def full_scrape(out_file: str)->None:
    pass
    # scrape it all out

    #save it
