from tools import configs
from tools.configs import path_define
from tools.services import upgrade_service


def main() -> None:
    upgrade_service.upgrade_ark_pixel()

    for upgrade_config in configs.UPGRADE_CONFIGS:
        upgrade_service.upgrade_fonts(upgrade_config)

    for file_path in path_define.FONTS_DIR.rglob('*.txt'):
        if not file_path.is_file():
            continue

        text = file_path.read_text('utf-8')
        file_path.write_text(text, 'utf-8')


if __name__ == '__main__':
    main()
