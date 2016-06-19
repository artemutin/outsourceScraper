import sources.FarpostDictionaryScraper as F
import sources.GisDictionaryScraper as G
import csv
from logging import info
from typing import List
from re import sub
from functools import partial, reduce
import concurrent.futures as fut

from sources.utils import catalogs, cities


def for_fut(Sc, city, page):
    ads = []
    i = 1
    while True:
        info('parsing page {}'.format(i))
        scraper = Sc(page=page, city=city, region=27)
        # print(page.page)
        ads.extend(scraper.ads)
        page = page.go_next()
        i += 1
        if not page: break

    return ads


def scrape_catalog(catalog: str, category: str, city: str)->List[dict]:
    if catalog == 'vl':
        urls = catalogs.get(catalog).get(category)
        if city == 'Хабаровск':
            urls = map(lambda x: sub(".*\.ru", "http://www.dvhab.ru", x), urls)
        pages = map(F.CatalogPage, urls)
        Sc = partial(F.FarpostDictionaryScraper, keywords={'scrape_details': True})
    elif catalog == '2gis':
        pages = map(lambda cat: G.CatalogPage('https://2gis.ru/{city}/{category}'.format(city=cities.get(city),
                                                                      category=cat)), catalogs.get(catalog).get(category))
        Sc = partial(G.GisDictionaryScraper, keywords={'scrape_details': True})

    ads = []
    with fut.ThreadPoolExecutor(max_workers=4) as executor:
        ads = executor.map(
            partial(for_fut, Sc, city),
            pages
        )
        ads = reduce(lambda x, y: x+y, list(ads) )
        return ads


def unzip_dict(d: dict):
    date = d.get('renewDate', None)
    if date:
        d['renewDate'] = date.isoformat()

    address = d.get('address', None)
    if address:
        d.update(address)
        del d['address']

    return d


def full_scrape(out_file: str)->None:
    with open(out_file, 'w') as csvfile:
        field_names = ['firmTitle', 'catalogURL', 'labeledCategory', 'category', 'renewDate', 'firmShortDesc',
                       'phone', 'email', 'site', 'region', 'city', 'rest', 'promoted', 'firmAdvertisement']
        writer = csv.DictWriter(csvfile, field_names)
        # Farpost scrape
        for cat in catalogs['vl'].keys():
            for city in ['Владивосток', 'Хабаровск']:
                ads = scrape_catalog('vl', cat, city)
                ads = map(unzip_dict, ads)
                map(lambda ad: ad.update({'category': cat}), ads)
                writer.writeheader()
                writer.writerows(ads)
