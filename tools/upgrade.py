from tools.configs import UpgradeConfig
from tools.services import upgrade_service


def main():
    upgrade_service.upgrade_ark_pixel()

    for upgrade_config in UpgradeConfig.load():
        upgrade_service.upgrade_fonts(upgrade_config)


if __name__ == '__main__':
    main()
