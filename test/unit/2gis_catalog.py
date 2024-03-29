import unittest
from io import open
from os import chdir
from sys import path
from outsourceScraper.GisDictionaryScraper import *
from outsourceScraper.Catalog import scrape_catalog
from datetime import date
import re
import logging
import sys


class GisCatalog(unittest.TestCase):
    def setUp(self):
        chdir(path[0])
        f = open("../static/Карта Хабаровска_ улицы, дома и организации города — 2ГИС.html")
        self.page = f.read()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
        f.close()

    def testStatic(self):
        # created scraper from preloaded page
        scraper = GisDictionaryScraper(CatalogPage(self.page, is_url_page=True), 'Хабаровск', 27)
        ad_list = scraper.ads
        # read all ads from page
        self.assertEqual(len(ad_list), 12)

        # checked first one
        ad = ad_list[0]
        self.assertEqual(ad['firmTitle'], "1 Бухгалтерский центр, ООО, компания")
        self.assertEqual(ad['renewDate'], None)
        self.assertEqual(ad['firmShortDesc'],
                         'Бухгалтерское обслуживание, обучение, аудит, сопровождение'
                         )
        # self.assertEqual(ad['labeledCategory'], "Бухгалтерские услуги")
        self.assertEqual(ad['address'], {'region': 27, 'city': "Хабаровск", 'rest': "Ленина, 4"})
        self.assertEqual(ad['catalogURL'], 'https://2gis.ru/khabarovsk/firm/4926340373601068?queryState=center%2F135.065287%2C48.466025%2Fzoom%2F17')
        # it is promoted
        self.assertEqual(ad['promoted'], True)

    def testDetailedInfoLoad(self):
        # scrape of detailed info
        scraper = GisDictionaryScraper(CatalogPage(self.page, is_url_page=True) , 'Хабаровск', 27, True)
        for ad in scraper.ads:
            logging.info(ad)
            print("IN")
            # email is hidden even for registered user
            self.assertIsNotNone(ad['email'])
            self.assertTrue(ad['email'] == '')
            self.assertIsNotNone(ad['phone'])
            self.assertTrue(ad['phone'] == '' or re.match(r'[\d \(\)\+]+', ad['phone']))
            self.assertIsNotNone(ad['site'])
            self.assertTrue(ad['site'] == '' or re.search(r'http', ad['site']))
            if 'promoted' in ad.keys():
                self.assertIsNotNone(len(ad['firmAdvertisement']))

    def testDetailedPageScrape(self):
        page = BasePage('http://2gis.ru/khabarovsk/firm/4926340373421638?queryState=center%2F135.119353%2C48.474875%2Fzoom%2F17 ')
        ad = catalogue_page_parse(BeautifulSoup(page.page, 'html.parser'))
        self.assertIsNotNone(ad['email'])
        self.assertTrue(ad['email'] == '')
        self.assertIsNotNone(ad['phone'])
        self.assertTrue(ad['phone'] == '' or re.match(r'[\d \(\)\+]+', ad['phone']))
        self.assertIsNotNone(ad['site'])
        self.assertTrue(ad['site'] == '' or re.search(r'http', ad['site']))
        if 'promoted' in ad.keys():
            self.assertIsNotNone(len(ad['firmAdvertisement']))

    def testCatalogPage(self):
        # fake local page
        page = CatalogPage(self.page, is_url_page=True)
        self.assertEqual(page.num_pages, 13)
        # but it was only the first
        self.assertEqual(page.page_num, 1)

        # loaded page
        page = CatalogPage('https://2gis.ru/khabarovsk/search/', 'Бухгалтерские услуги')
        self.assertEqual(page.city, 'Хабаровск')
        # it has a lot more to be showed
        self.assertTrue(page.num_pages > 10)
        # but it was only the first
        self.assertEqual(page.page_num, 1)

        page.go_next()
        # but it was only the first
        self.assertEqual(page.page_num, 2)
        # check true url
        self.assertEqual(page.url, 'https://2gis.ru/khabarovsk/search/Бухгалтерские услуги/page/2/')

    def testfullCatalogScrape(self):
        logging.info('IN test')
        # ask to parse all catalogue
        results = scrape_catalog('2gis', category='Бухгалтерия', city='Хабаровск', num_pages=2)

        # ALERT: this test is unstable by definition
        self.assertEqual(len(results), 24)

