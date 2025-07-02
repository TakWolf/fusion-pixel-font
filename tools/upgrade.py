from tools import configs
from tools.services import upgrade_service


def main():
    upgrade_service.upgrade_ark_pixel()
    upgrade_service.setup_ark_pixel()

    for upgrade_config in configs.upgrade_configs:
        upgrade_service.upgrade_fonts(upgrade_config)


if __name__ == '__main__':
    main()
