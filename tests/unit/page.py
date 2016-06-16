import unittest
from io import open
from os import chdir
from sys import path
from sources.Page import Page


class PageTest(unittest.TestCase):

    def setUp(self):
        chdir(path[0])
        f = open("../static/Бухучёт во Владивостоке. Отзывы, цены, фото, карта.html")
        self.page = f.read()
        f.close()

    def testPage(self):
        # loaded page
        page = Page('http://www.vl.ru/spravochnik')
        # it has a lot more to be showed
        self.assertTrue(page.num_pages > 10)
        # but it was only the first
        self.assertEqual(page.page_num, 1)

        page.go_next()
        # but it was only the first
        self.assertEqual(page.page_num, 2)
        # check true url
        self.assertEqual(page.url, 'http://www.vl.ru/spravochnik?page=2')

