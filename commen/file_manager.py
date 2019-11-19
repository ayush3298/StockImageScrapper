import os


def check_and_create_if_folder_not_exists(self, path):
    if not os.path.isdir(path):
        os.makedirs(path)

    return True
