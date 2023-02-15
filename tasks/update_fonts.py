import logging

import configs
from services import update_service

logging.basicConfig(level=logging.DEBUG)


def main():
    for download_config in configs.download_configs:
        if download_config.is_enabled:
            update_service.update_font(download_config)


if __name__ == '__main__':
    main()
