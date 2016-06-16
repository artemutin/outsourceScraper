from sources.FarpostDictionaryScraper import *
from logging import info

catalogs = {
    'vl': {'Бухгалтерия': 'http://www.vl.ru/business/services-for-business/accountancy'}
}


def scrape_catalog(catalog, category):

    page = CatalogPage(catalogs.get(catalog).get(category))
    ads = []
    i = 1
    while True:
        info('parsing page {}'.format(i))
        scraper = FarpostDictionaryScraper(page.page)
        # print(page.page)
        ads.extend(scraper.ads)
        i += 1
        page = page.go_next()
        if not page: break

    return ads
