import unittest
from sources.Page import BasePage


class PageTest(unittest.TestCase):

   def testBasePage(self):
       page = BasePage('http://google.ru')
       self.assertEqual(page.url, 'http://google.ru')
       self.assertIsNone(page.go_next())




