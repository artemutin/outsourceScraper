import outsourceScraper.FarpostDictionaryScraper as F
import outsourceScraper.GisDictionaryScraper as G
import csv
from logging import info
from typing import List
from re import sub
from functools import partial, reduce
import concurrent.futures as fut
from math import inf

from outsourceScraper.utils import catalogs, cities, cities_to_region


def for_fut(Sc, city, num_pages, page):
    ads = []
    i = 1
    while i <= num_pages:
        info('parsing page {}'.format(i))
        region = cities_to_region.get(city, 00)
        scraper = Sc(page=page, city=city, region=region)
        # print(page.page)
        try:
            ads.extend(scraper.ads)
        except Exception:
            info("for some reason couldn't extend with new ads piece, page {}".format(i))
        page = page.go_next()
        i += 1
        if not page: break

    return ads


def scrape_catalog(catalog: str, category: str, city: str, num_pages: int = inf)->List[dict]:
    if catalog == 'vl':
        urls = catalogs.get(catalog).get(category)
        if city == 'Хабаровск':
            urls = map(lambda x: sub(".*\.ru", "http://www.dvhab.ru", x), urls)
        pages = map(F.CatalogPage, urls)
        Sc = partial(F.FarpostDictionaryScraper, scrape_details = True)
    elif catalog == '2gis':
        pages = map(lambda cat: G.CatalogPage('https://2gis.ru/{city}/{category}'.format(city=cities.get(city),
                                                                      category=cat)), catalogs.get(catalog).get(category))
        Sc = partial(G.GisDictionaryScraper, scrape_details=True)

    ads = []
    max_workers = 3
    if catalog == 'vl':
        max_workers = 10
    elif catalog == '2gis':
        max_workers = 3
    with fut.ThreadPoolExecutor(max_workers=max_workers) as executor:
        ads = executor.map(
            partial(for_fut, Sc, city, num_pages),
            pages
        )
        ads = reduce(lambda x, y: x+y, list(ads) )
        return ads


def unzip_dict(d: dict):
    try:
        date = d.get('renewDate', None)
    except Exception as e:
        print(e)

    if date:
        d['renewDate'] = date.isoformat()

    address = d.get('address', None)
    if address:
        d.update(address)
        del d['address']

    return d


def full_scrape(out_file: str)->None:
    with open(out_file, 'w') as csvfile:
        field_names = ['firmTitle', 'catalogURL', 'catalog', 'labeledCategory', 'category', 'firmShortDesc', 'site',
                       'renewDate', 'clicks', 'promoted', 'firmAdvertisement', 'phone', 'email', 'region', 'city', 'rest']
        writer = csv.DictWriter(csvfile, field_names)
        writer.writeheader()
        # Farpost scrape

        for cat in catalogs['vl']:
            for city in ['Владивосток', 'Хабаровск']:
                ads = list(scrape_catalog('vl', cat, city))
                ads = list(filter(lambda x: x is not None, ads))
                for ad in ads:
                    ad = unzip_dict(ad)
                    ad.update({'category': cat, 'catalog': 'vl'})
                    if city == 'Хабаровск':
                        ad.update({'region': 27})

                writer.writerows(ads)

        # 2gis

        for cat in catalogs['2gis']:
        # cat = 'IT'
            for city in ['Владивосток', 'Хабаровск']:
                ads = list(scrape_catalog('2gis', cat, city))
                ads = list(filter(lambda x: x is not None, ads))

                for ad in ads:
                    ad = unzip_dict(ad)
                    ad.update({'category': cat, 'catalog': '2gis'})

                writer.writerows(ads)
