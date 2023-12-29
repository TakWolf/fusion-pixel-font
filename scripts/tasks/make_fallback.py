import logging

from scripts import configs
from scripts.configs import path_define
from scripts.services import dump_service
from scripts.utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.fallback_glyphs_dir)

    for font_config in configs.font_configs:
        fallback_configs = configs.font_size_to_fallback_configs[font_config.size]
        for fallback_config in fallback_configs:
            dump_service.apply_fallback(fallback_config)


if __name__ == '__main__':
    main()
