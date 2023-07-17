import logging

from configs import UpdateConfig
from services import update_service

logging.basicConfig(level=logging.DEBUG)


def main():
    update_configs = UpdateConfig.load()
    for update_config in update_configs:
        update_service.update_fonts(update_config)


if __name__ == '__main__':
    main()
