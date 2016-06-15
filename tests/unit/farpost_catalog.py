import unittest
from io import open
from os import chdir
from sys import path
from sources.FarpostDictionaryScraper import *
from datetime import date

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
        self.assertEqual(ad['address'], Address(region=25, city="Владивосток", left="пр-кт Красного Знамени, 59"))


