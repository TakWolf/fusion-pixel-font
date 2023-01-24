import logging
import os

from configs import path_define
from services import publish_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.make_dirs_if_not_exists(path_define.docs_dir)

    publish_service.copy_docs_files()


if __name__ == '__main__':
    main()
