import unittest
import logging
import sys
from os import remove, listdir
from sources.Catalog import full_scrape


class FullScrape(unittest.TestCase):
    def testIt(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

        log_name = 'FullScrape.log'
        ch = logging.StreamHandler()
        csv_name = 'results.csv'
        if log_name in listdir():
            remove(log_name)
        if csv_name in listdir():
            remove(csv_name)
        self.assertTrue(log_name not in listdir())
        self.assertTrue(csv_name not in listdir())
        logging.basicConfig(filename=log_name, level=logging.DEBUG)

        full_scrape(csv_name)

        # self.assertTrue(log_name in listdir())
        self.assertTrue(csv_name in listdir())