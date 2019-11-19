import requests
from requests.exceptions import MissingSchema
from tqdm import tqdm


def download_image(self, url):
    try:
        folder = self.image_store_dir + '/'
        local_filename = (folder + url.split('/')[-1]).replace('//', '/')
        # NOTE the stream=True parameter below
        if url.split('/')[-1] not in self.downloaded_images:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in tqdm(r.iter_content(chunk_size=1000)):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            # f.flush()
            self.downloaded_images.append(url.split('/')[-1])
            with open(self.downloaded_image_url_file, 'a') as f:
                f.write(url.split('/')[-1] + '\n')
            return local_filename
        else:
            print(url.split('/')[-1] + ' Downloaded')
    except MissingSchema:
        pass


def download_from_file(self, filename, use_concurancy=True):
    with open(filename) as f:
        print(filename)
        images = [n.replace('\n', '') for n in f.readlines()]
    for image in images:
        download_image(self, image)


def get_already_downloaded_images(self):
    try:
        with open(self.downloaded_image_url_file) as f:
            return [a.replace('\n', '') for a in f.readlines()]
    except FileNotFoundError:
        with open(self.downloaded_image_url_file, 'w') as f:
            pass
        return []
