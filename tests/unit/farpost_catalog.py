import unittest
from io import open
from os import chdir
from sys import path
from sources.FarpostDictionaryScraper import *
from sources.Catalog import scrape_catalog
from datetime import date
import logging


class FarpostCatalog(unittest.TestCase):

    def setUp(self):
        chdir(path[0])
        f = open("../static/Бухучёт во Владивостоке. Отзывы, цены, фото, карта.html")
        self.page = f.read()
        f.close()

    def testStatic(self):
        # created scraper from preloaded page
        scraper = FarpostDictionaryScraper(self.page)
        ad_list = scraper.ads
        # read all ads from page
        self.assertEqual(len(ad_list), 30)

        # checked first one
        ad = ad_list[0]
        self.assertEqual(ad['firmTitle'], "Мой бизнес")
        self.assertEqual(ad['renewDate'], date(2016, 5, 30))
        self.assertEqual(ad['firmShortDesc'], ('Компания оказывает комплекс услуг по сопровождению бизнеса - регистрация ООО, ИП, '
            'ликвидация, полное бухгалтерское сопровождение, '
            'оценка работы бухгалтеров, ЭЦП для сдачи отчетности, 1С, CRM-системы управления '
            'бизнесом, онлайн бизнес-консультации.')
                         )
        self.assertEqual(ad['labeledCategory'], "Бухгалтерско-юридическая компания")
        self.assertEqual(ad['address'], {'region': 25, 'city': "Владивосток", 'rest': " пр-кт Красного Знамени, 59"})
        self.assertEqual(ad['catalogURL'], 'http://www.vl.ru/mybusinesson')

        # checked all dates, just in case
        dates = [date(2016, 5, 30), date(2016, 4, 17), date(2016, 4, 24), date(2016, 6, 1), date(2016, 3, 23), date(2016, 4, 22),
                 date(2016, 5, 25), date(2016,4,13), date(2016,6,7), date(2016,5,11),date(2016,3,28), date(2016,3,23),
                 date(2016,3,23),date(2016,3,2),date(2016,6,10),date(2016,5,26),date(2016,5,23),date(2016,5,20),date(2016,5,16),
                 date(2016,5,11),date(2016,5,6),date(2016,5,6),date(2016,4,28),date(2016,4,13),date(2016,3,23),date(2016,3,9),
                 date(2016,6,7),date(2016,6,3),date(2016,5,30),date(2016,5,27)]
        for i in range(0, 30):
            self.assertEqual(ad_list[i]['renewDate'], dates[i])

    def testMultiplePages(self):
        scraper = FarpostDictionaryScraper(self.page)

    def testCataloguePageParse(self):
        # now test parse results for inner catalogue pages
        f = open("../static/Мой бизнес_ отзывы, цены, фото, карта. Владивосток, Приморский край.html")
        page = f.read()
        f.close()

        d = catalogue_page_parse(BeautifulSoup(page, 'html.parser'))
        self.assertEqual(d, {'site': 'http://www.mybusinesson.pro', 'email': 'm.ivanov@mybusinesson.pro',
                                             'phone': '+7(423) 206-00-42'})

    def testCatalogPage(self):
        # loaded page
        page = CatalogPage('http://www.vl.ru/spravochnik')
        # it has a lot more to be showed
        self.assertTrue(page.num_pages > 10)
        # but it was only the first
        self.assertEqual(page.page_num, 1)

        page.go_next()
        # but it was only the first
        self.assertEqual(page.page_num, 2)
        # check true url
        self.assertEqual(page.url, 'http://www.vl.ru/spravochnik?page=2')

    def testfullCatalogScrape(self):
        logging.info('IN test')
        # ask to parse all catalogue
        results = scrape_catalog('vl', category='Бухгалтерия')

        # ALERT: this test is unstable by definition
        self.assertEqual(len(results), 5*30 + 4)


