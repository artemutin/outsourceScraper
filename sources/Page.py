from requests import request
from urllib.request import unquote
from re import split


class BasePage:
    def __init__(self, url):
        self.url = unquote(split(r'\?', url)[0])+'/'
        response = request('GET', url, headers={'User-agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            raise Exception('network error: code {}'.format(response.status_code))
        else:
            self.page = response.text

    def go_next(self):
        return None


