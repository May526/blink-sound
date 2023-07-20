import os
import sys

def get_package_root() -> str:
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def get_pj_root() -> str:
    return os.path.dirname(get_package_root())


def get_data_root() -> str:
    return get_pj_root() + "/data"
