import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self):
        self.session = requests.session()
        self.base_url = 'https://www.pexels.com'

    def make_query(self):
        try:
            res = self.session.get("https://www.pexels.com/search/business%20woman/")
            with open('pexel.html', 'w', encoding='utf8') as f:
                f.write(res.text)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                self.get_all_images(soup)
        except Exception as e:
            print(e)

    def get_from_file(self):
        with open('pexel.html', 'r', encoding='utf8') as f:
            data = f.read()
            soup = BeautifulSoup(data, 'lxml')
            self.get_all_images(soup)

    def get_all_images(self, soup):
        items = soup.find_all('img', {'class': 'photo-item__img'})
        image_urls = [item['data-big-src'].split('?')[0] for item in items]


s = Scrapper()
s.get_from_file()
