from unittest import TestCase
import csv
import os


class CSVOutput(TestCase):
    out_file = "test.csv"

    def testWrite(self):
        self.assertTrue(self.out_file not in os.listdir())
        with open(self.out_file, 'w') as csvfile:
            field_names = ['Hello']
            writer = csv.DictWriter(csvfile, field_names)
            writer.writerow({'Hello': 1})

        self.assertTrue(self.out_file in os.listdir())

    def tearDown(self):
        os.remove(self.out_file)
