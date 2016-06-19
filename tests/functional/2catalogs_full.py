import unittest
import logging
from os import remove, listdir
from sources.Catalog import full_scrape


class FullScrape(unittest.TestCase):
    def testIt(self):
        logging.basicConfig(format='%(asctime)s %(message)s')
        log_name = 'FullScrape.log'
        csv_name = 'results.csv'
        if log_name in listdir():
            remove(log_name)
        if csv_name in listdir():
            remove(csv_name)
        self.assertTrue(log_name not in listdir())
        self.assertTrue(csv_name not in listdir())
        logging.basicConfig(filename=log_name, level=logging.INFO)

        full_scrape(csv_name)

        self.assertTrue(log_name in listdir())
        self.assertTrue(csv_name in listdir())