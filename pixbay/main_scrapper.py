import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self):
        self.session = requests.session()
        self.base_url = 'https://pixabay.com/'

    def make_query(self):
        try:
            res = self.session.get("https://pixabay.com/images/search/business%20woman/")
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                self.get_all_images(soup)
        except Exception as e:
            print(e)

    def get_all_images(self, soup):
        items = soup.find_all('div', {'class': 'item'})
        items_url = [item.find('a')['href'] for item in items]
        self.download_each_image(items_url)

    def download_each_image(self, list_of_urls):
        pass


s = Scrapper()
# s.make_query()
