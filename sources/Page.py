from requests import request
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url):
        self.url = url
        response = request('GET', url)
        if response.status_code != 200:
            raise Exception('network error: code {}'.format(response.status_code) )
        else:
            self.page = response.text
            self._bs = BeautifulSoup(self.page, 'html.parser')
            num = self._bs.find('a', id='link-last')
            if num:
                self.num_pages = int(num.text)
            else:
                self.num_pages = 1

            self.page_num = int(self._bs.find('li', class_='current').text)

    def go_next(self):
        if self.num_pages > self.page_num:
            self.__init__(self._bs.find('li', class_='current').next_sibling.a['href'])
        return self