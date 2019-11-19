import concurrent
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from commen.file_manager import check_and_create_if_folder_not_exists
from commen.Downloader import download_from_file, get_already_downloaded_images


class Scrapper:
    def __init__(self, query):
        self.session = requests.session()
        self.base_url = 'https://www.pexels.com'
        self.XMLHttpRequestHeaders = {
            'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
            'accept': "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            'accept-language': "en-GB,en;q=0.5",
            'x-csrf-token': "h+FF40ni1fmQeZPHR1rlSzOavPxroerIgeMI/C+gkk71SJs1njYsDYzlhjR7dfj49oBcsvSdJRhKuixX47AGbA==",
            'x-requested-with': "XMLHttpRequest",
            'connection': "keep-alive",
            'referer': "https://www.pexels.com/search/business%20woman/",
            'cookie': "__cfduid=d676722265c19abea848a6b0a1f72f6ea1573799765; locale=en-US; _pexels_session=amR5QlJodlFxb2tRTGY3WHVGSnBGWXRERDVlUjFTVHlsNmpWcGtKQyttekRiMVZEUFRzdXQyV3NlNmdjM2pNNThpM1lEMmExcDdZZlh4QlFMc0pyMURNLzNEdzRkaURhOC9sdHl1aDJpamJQK1p6N2ZYZGF5MndCRXZxQzQrMDZLRWlLOXdBeTdzSDZqZDVYeVBGUERBPT0tLXZ4aExydVlZd1U2Ti8ranZuc25yOHc9PQ%3D%3D--00f81083c52c253d0a2134603ecfac1fa2fbcda3",
            'pragma': "no-cache",
            'cache-control': "no-cache",
            'te': "Trailers",
            'postman-token': "4cad8ad0-2c2e-804f-ed7d-e5dbc9eb61dc"
        }
        self.page = 1
        self.query = query
        self.images_urls = []
        self.dir = os.getcwd()
        self.image_store_dir = self.dir + '/result/Images'
        self.image_url_file = self.dir + '/result/all_images.txt'
        self.downloaded_image_url_file = self.dir + '/result/downloaded_images.txt'
        check_and_create_if_folder_not_exists(self, os.getcwd() + '/result')
        check_and_create_if_folder_not_exists(self, self.image_store_dir)

        self.downloaded_images = get_already_downloaded_images(self)

    def make_query(self, ):
        try:
            res = self.session.get(f"https://www.pexels.com/search/{self.query}/?page=" + str(self.page))
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                self.get_all_images(soup)
                next = [int(a.text) for a in soup.find_all('a') if '?page=' in str(a) and a.text.isdigit()]
                next = max(next)
                next = range(1, next)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = list(tqdm(executor.map(self.get_all_images, next), total=len(next)))
                    return results
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            traceback.print_exc()

    def get_all_images(self, page):
        try:
            res = self.session.get(f"https://www.pexels.com/search/{self.query}/?page=" + str(page))
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                items = soup.find_all('img', {'class': 'photo-item__img'})
                with open(self.image_url_file, 'a', newline='\n') as f:
                    f.write('\n')
                    f.write('\n'.join([item['data-big-src'].split('?')[0] for item in items]))


        except Exception as e:
            traceback.print_tb(e.__traceback__)
            traceback.print_exc()


s = Scrapper('computer')
# s.make_query()
download_from_file(s, s.image_url_file)
