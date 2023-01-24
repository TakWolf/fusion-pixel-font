import logging
import os
import shutil

from configs import path_define
from services import publish_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.www_dir)
    shutil.copytree(path_define.www_static_dir, path_define.www_dir)

    publish_service.copy_www_files()
    publish_service.deploy_www()


if __name__ == '__main__':
    main()
