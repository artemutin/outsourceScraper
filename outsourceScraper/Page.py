from requests import request


class BasePage:
    def __init__(self, url, **kwargs):
        self.url = url
        self.response = request('GET', url, headers={'User-agent': 'Mozilla/5.0'}, cookies=kwargs.get('cookies', {}))
        if self.response.status_code != 200 and not self.response.is_redirect:
            raise Exception('network error: url {}, code {}'.format(url, self.response.status_code))
        else:
            self.page = self.response.text

    def go_next(self):
        return None


