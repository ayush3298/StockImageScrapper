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
        self.session.headers = {
            'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'accept-language': "en-GB,en;q=0.5",
            'content-type': "application/x-www-form-urlencoded",
            'Host': "pixabay.com",
            'connection': "keep-alive",
            # 'referer': "https://pixabay.com/accounts/login/",
            # 'cookie': "__ client_width=1354; is_human=1; dwf_attribution_template_ads=False; anonymous_user_id=e646f756-b06c-47b0-b8af-72861304961d; csrftoken=VPZWQMHGH1XtPMOEgmoMKNJdAE4sb0dlmRxQzHG2P5tP4C2Zr5LCeNmjnQJtdWse; sessionid=\"eyJ0ZXN0Y29va2llIjoid29ya2VkIn0:1iXL6e:JQybSCvCzfrI0Oqwd9oNHveYEeQ\"",
            'upgrade-insecure-requests': "1",
            'pragma': "no-cache",
            'cache-control': "no-cache",
        }
        self.session.get(self.base_url)
        print(dict(self.session.cookies))
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

    def login(self):
        headers = {
            'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'accept-language': "en-GB,en;q=0.5",
            'content-type': "application/x-www-form-urlencoded",
            'origin': "https://pixabay.com",
            'connection': "keep-alive",
            'referer': "https://pixabay.com/accounts/login/",
            'cookie': "__cfduid=dd9d8ee28abd95b326f41bd7f14cdd2611567770787; client_width=1354; is_human=1; dwf_attribution_template_ads=False; anonymous_user_id=e646f756-b06c-47b0-b8af-72861304961d; csrftoken=VPZWQMHGH1XtPMOEgmoMKNJdAE4sb0dlmRxQzHG2P5tP4C2Zr5LCeNmjnQJtdWse; sessionid=\"eyJ0ZXN0Y29va2llIjoid29ya2VkIn0:1iXL6e:JQybSCvCzfrI0Oqwd9oNHveYEeQ\"",
            'upgrade-insecure-requests': "1",
            'pragma': "no-cache",
            'cache-control': "no-cache",
            'te': "Trailers",
            'postman-token': "cf25fce8-15b8-343b-8055-a40fc974b9ac"
        }
        data = {"Form data": {"username": "abairagi311@gmail.com", "password": "8461034077",
                              "csrfmiddlewaretoken": "pWE73hVYb0Ltc0ZQl4UiWxoYxvL4u6L9ekLAExdz0TgAKLzbsDrjuDL7iDPQchGh",
                              "next": ""}}
        res = self.session.post('https://pixabay.com/accounts/login/', data=data, headers=headers)
        print(res)

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
        print(self.total_pages)
        for i in range(self.total_pages - 1):
            data = {'key': self.api_key, 'q': self.query, 'image_type': 'photo', 'page': self.page}
            res = self.session.get(self.base_url, params=data)
            if res.status_code == 200:
                data = res.json()
                for hit in data['hits']:
                    with open(self.image_url_file, 'a') as f:
                        f.write(hit['largeImageURL'] + '\n')
            self.page += 1


s = Scrapper('computer')
s.login()
# s.get_total_pages()
# s.get_all_images()
# download_from_file(s, s.image_url_file)
