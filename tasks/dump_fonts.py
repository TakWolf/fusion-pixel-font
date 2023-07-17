import logging

from configs import path_define
from services import dump_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.dump_dir)

    dump_service.dump_fonts()


if __name__ == '__main__':
    main()
