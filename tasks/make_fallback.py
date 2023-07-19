import logging

from configs import path_define
from configs.fallback_config import FallbackConfig
from services import dump_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.fallback_glyphs_dir)

    fallback_configs = FallbackConfig.load()
    for fallback_config in fallback_configs:
        dump_service.apply_fallback(fallback_config)


if __name__ == '__main__':
    main()
