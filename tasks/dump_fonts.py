import logging

from configs import path_define
from configs.dump_config import DumpConfig
from services import dump_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.dump_dir)

    dump_configs = DumpConfig.load()
    for dump_config in dump_configs:
        dump_service.dump_font(dump_config)


if __name__ == '__main__':
    main()
