import logging

import configs
from configs import path_define
from services import dump_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.dump_dir)

    for font_config in configs.font_configs:
        dump_configs = configs.font_size_to_dump_configs[font_config.size]
        for dump_config in dump_configs:
            dump_service.dump_font(dump_config)


if __name__ == '__main__':
    main()
