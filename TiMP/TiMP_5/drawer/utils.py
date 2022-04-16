import os


def mkdir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)


def check_path(path: str):
    """ Create all folders """
    mkdir('/'.join(path.split('/')[:-1]))
