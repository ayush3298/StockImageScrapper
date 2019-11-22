import os
import configparser
import logging
import os
import time
import traceback
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from tqdm import tqdm

from commen.Downloader import get_already_downloaded_images
from commen.file_manager import check_and_create_if_folder_not_exists


class Scrapper:
    def __init__(self):
        self.session = requests.session()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.base_url = 'https://picspree.com'
        self.page = 1
        self.total_pages = 1
        self.proxy = {'http': config['configuration']['proxy'], 'https': config['configuration']['proxy']}
        self.query = config['configuration']['query']
        self.images_urls = []
        self.dir = os.getcwd()
        self.log_file = self.dir + 'logs.log'
        self.logger = logging
        self.logger.basicConfig(filename=self.log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
        self.image_store_dir = self.dir + '/result/Images'
        self.image_url_file = self.dir + '/result/all_images.txt'
        self.downloaded_image_url_file = self.dir + '/result/downloaded_images.txt'
        check_and_create_if_folder_not_exists(self, os.getcwd() + '/result')
        check_and_create_if_folder_not_exists(self, self.image_store_dir)
        self.downloaded_images = get_already_downloaded_images(self)

    def get_total_pages(self):
        try:
            res = self.session.get('https://picspree.com/en/search/' + self.query)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                page_count = soup.find('span', {'class': 'paging-count'})
                if page_count:
                    page_count = int(page_count.text.split('of')[-1].strip())
                    self.total_pages = page_count
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            traceback.print_exc()
            self.logger.exception(e)

    def get_all_images(self):
        print(self.total_pages)
        for i in tqdm(range(self.total_pages)):
            successful = False
            while not successful:
                try:
                    data = {'page': self.page}
                    res = self.session.get('https://picspree.com/en/search/' + self.query, params=data)
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.text, 'lxml')
                        for a in soup.find_all('a', {'class': 'thumbnail-download-link'}):
                            with open(self.image_url_file, 'a') as f:
                                f.write(self.base_url + a['href'] + '\n')
                    self.page += 1
                    successful = True
                except ConnectionError as e:
                    self.logger.exception(e)
                    print('Please Connect with the internet.')
                    time.sleep(10)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    traceback.print_exc()
                    self.logger.exception(e)

    def download_image(self, url):
        try:
            folder = self.image_store_dir + '/'
            local_filename = (folder + url.split('/')[-1]).replace('//', '/') + '.jpg'
            if url.split('/')[-1] not in self.downloaded_images:
                res = requests.get(url, allow_redirects=False, proxies=self.proxy)
                with requests.get(res.headers['Location'], stream=True, allow_redirects=False) as r:
                    if r.status_code != 429:
                        r.raise_for_status()
                        with open(local_filename, 'wb') as f:
                            for chunk in tqdm(r.iter_content(chunk_size=1000)):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)
                        #                 f.flush()
                        self.downloaded_images.append(url.split('/')[-1])
                        with open(self.downloaded_image_url_file, 'a') as f:
                            f.write(url.split('/')[-1] + '\n')
                        return local_filename
                    else:
                        time.sleep(20)
                        print('Too many requests, Sleeping for 20 seconds.')
                        self.download_image(self, url)

            else:
                print(url.split('/')[-1] + ' Downloaded')

        except requests.exceptions.MissingSchema:
            pass
        except Exception as e:
            self.logger.exception(e)
            self.download_image(url)

    def download_from_file(self):
        with open(self.image_url_file) as f:
            images = [n.replace('\n', '') for n in f.readlines()]
        for image in tqdm(images):
            self.download_image(image)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.get_total_pages()
    scrapper.get_all_images()
    scrapper.download_from_file()
