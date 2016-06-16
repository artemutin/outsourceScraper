from sources.FarpostDictionaryScraper import *

catalogs = {
    'vl': {'Бухгалтерия': 'http://www.vl.ru/business/services-for-business/accountancy'}
}

def scrape_catalog(catalog, category):
    pass
    page = CatalogPage(catalogs.get(catalog).get(category))
    scraper = FarpostDictionaryScraper(page.page)