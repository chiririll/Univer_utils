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


def copy_file(src: str, dst: str):
    f_src = open(src, 'rb')
    f_dst = open(dst, 'wb')

    f_dst.write(f_src.read())

    f_dst.close()
    f_src.close()
