import logging

import configs
from services import update_service

logging.basicConfig(level=logging.DEBUG)


def main():
    for update_config in configs.update_configs:
        update_service.update_fonts(update_config)


if __name__ == '__main__':
    main()
