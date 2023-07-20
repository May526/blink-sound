import os


def get_package_root() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_pj_root() -> str:
    return os.path.dirname(get_package_root())


def get_data_root() -> str:
    return get_pj_root() + "/data"