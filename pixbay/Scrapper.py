import concurrent
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from commen.file_manager import check_and_create_if_folder_not_exists
from commen.Downloader import download_from_file, get_already_downloaded_images
from pprint import pprint


class Scrapper:
    def __init__(self, query):
        self.session = requests.session()
        self.base_url = 'https://pixabay.com/api/'
        self.api_key = '6698420-d136525310ae017fe87ca6b4d'
        self.page = 1
        self.total_pages = 1
        self.query = query
        self.images_urls = []
        self.dir = os.getcwd()
        self.image_store_dir = self.dir + '/result/Images'
        self.image_url_file = self.dir + '/result/all_images.txt'
        self.downloaded_image_url_file = self.dir + '/result/downloaded_images.txt'
        check_and_create_if_folder_not_exists(self, os.getcwd() + '/result')
        check_and_create_if_folder_not_exists(self, self.image_store_dir)

        self.downloaded_images = get_already_downloaded_images(self)

    def get_total_pages(self):
        try:
            data = {'key': self.api_key, 'q': self.query, 'image_type': 'photo', 'page': self.page}
            res = self.session.get(self.base_url, params=data)
            if res.status_code == 200:
                data = res.json()
                self.total_pages = round(data['total'] / data['totalHits'])
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            traceback.print_exc()

    def get_all_images(self):
        for i in range(self.total_pages - 1):
            data = {'key': self.api_key, 'q': self.query, 'image_type': 'photo', 'page': self.page}
            res = self.session.get(self.base_url, params=data)
            if res.status_code == 200:
                data = res.json()
                for hit in data['hits']:
                    with open(self.image_url_file, 'a') as f:
                        f.write(hit['largeImageURL'])
            self.page += 1


s = Scrapper('computer')
s.get_total_pages()
s.get_all_images()
# download_from_file(s, s.image_url_file)
