import requests

from fake_useragent import UserAgent
class BaseCrawler():
    """
    爬虫：
    """
    def __init__(self, driver, save_path=None):
        self.base_url = None
        self.save_path = save_path
        if save_path is None:
            self.save_path = 'result'

        self.user_agent = UserAgent()
        self.header = {
            # 'User-Agent': self.user_agent.chrome
            'User-Agent': self.user_agent.random

        }


    def get(self, url, headers=None):
        if headers is None:
            headers = self.header
        return requests.get(url=url, headers=headers)

    def parse_book_list(self, list_url):
        pass

    def parse_book_detail(self, detail_url):
        pass

    def writer(self):
        pass



