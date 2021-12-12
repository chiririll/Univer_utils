import os


def parse_task(task: str) -> dict:
    # TODO
    return task


def mkdir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)


def check_path(path: str):
    """ Create all folders """
    mkdir('/'.join(path.split('/')[:-1]))


def clear_folder(path: str):
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            clear_folder(f)
        else:
            os.remove(f)
