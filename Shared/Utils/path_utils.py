import os


def create_folders(path_str: str | os.PathLike[str]):
    folders = path_str.split('/')[:-1]

    for i in range(len(folders)):
        part = '/'.join(folders[0:i+1])
        if not os.path.isdir(part):
            os.mkdir(part)


def walk(folder: str | os.PathLike[str], base_path: str = ''):
    def check_path(path):
        if len(path) > 0 and path[-1] != '/':
            path += '/'
        return path

    files = []

    folder = check_path(folder)
    base_path = check_path(base_path)

    for f in os.listdir(folder):
        if os.path.isdir(folder + f):
            files += walk(folder + f + '/', base_path + f + '/')
        else:
            files.append(base_path + f)
    return files
