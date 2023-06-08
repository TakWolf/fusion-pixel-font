import logging

import configs
from services import update_service

logging.basicConfig(level=logging.DEBUG)


def main():
    for download_config in configs.download_configs:
        update_service.update_fonts(download_config)
    update_service.update_chill_bitmap_license()


if __name__ == '__main__':
    main()
