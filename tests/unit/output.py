from unittest import TestCase
import csv
import os
from sources.Catalog import scrape_catalog, unzip_dict
from re import match, IGNORECASE
import logging
from sources.utils import setupStdoutLog


class CSVOutput(TestCase):
    out_file = "test.csv"

    def testWrite(self):
        self.assertTrue(self.out_file not in os.listdir())
        with open(self.out_file, 'w') as csvfile:
            field_names = ['Hello']
            writer = csv.DictWriter(csvfile, field_names)
            writer.writerow({'Hello': 1})

        self.assertTrue(self.out_file in os.listdir())

    def testFarpostCatalogCSV(self):
        setupStdoutLog()
        with open(self.out_file, 'w') as csvfile:
            field_names = ['firmTitle', 'catalogURL', 'catalog', 'labeledCategory', 'category', 'firmShortDesc', 'site',
                           'renewDate', 'clicks', 'promoted', 'firmAdvertisement', 'phone', 'email', 'region', 'city',
                           'rest']
            writer = csv.DictWriter(csvfile, field_names)
            writer.writeheader()

            cat = 'Бухгалтерия'
            ads = list(scrape_catalog('vl', cat, 'Владивосток', num_pages=1))
            ads = list(filter(lambda x: x is not None, ads))
            for ad in ads:
                ad = unzip_dict(ad)
                ad.update({'category': cat, 'catalog': 'vl'})

            writer.writerows(ads)

        with open(self.out_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, field_names)
            self.assertEqual(set(reader.__next__().values()), set(field_names) )
            for row in reader:
                logging.info(str(row))
                self.assertTrue(match(r'[\w ,\.]+', row['firmTitle'], IGNORECASE))
                self.assertTrue(row['clicks'] == '' or match(r'\d+', row['clicks']))
                self.assertTrue(row['promoted'] == '')
                self.assertTrue(match(r'.*?vl.*?\.ru.*', row['catalogURL']))
                self.assertTrue(row['site'] == '' or match(r'http.*?\.[\w]{1,5}', row['site']))

    def tearDown(self):
        os.remove(self.out_file)
