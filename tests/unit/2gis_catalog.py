import unittest
from io import open
from os import chdir
from sys import path
from sources.GisDictionaryScraper import *
from sources.Catalog import scrape_catalog
from datetime import date
import re
import logging


class GisCatalog(unittest.TestCase):
    def setUp(self):
        chdir(path[0])
        f = open("../static/Карта Хабаровска_ улицы, дома и организации города — 2ГИС.html")
        self.page = f.read()
        f.close()

    def testStatic(self):
        # created scraper from preloaded page
        scraper = GisDictionaryScraper(self.page, 'Хабаровск', 27)
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
        scraper = GisDictionaryScraper(self.page, 'Хабаровск', 27, True)
        for ad in scraper.ads:
            logging.info(ad)
            # email is hidden even for registered user
            self.assertIsNotNone(ad['email'])
            self.assertTrue(ad['email'] == '')
            self.assertIsNotNone(ad['phone'])
            self.assertTrue(ad['phone'] == '' or re.match(r'[\d\ \(\)\+]+', ad['phone']))
            self.assertIsNotNone(ad['site'])
            self.assertTrue(ad['site'] == '' or re.search(r'http', ad['site']))
