import os


def bool_params_to_string(params: dict) -> dict:
    params_str = {}
    for k, v in params.items():
        if type(v) is bool:
            params_str[k] = "ИСТИНА" if v else "ЛОЖЬ"
        else:
            params_str[k] = v
    return params_str


def clear_folder(path: str):
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            clear_folder(f)
        else:
            os.remove(f)
