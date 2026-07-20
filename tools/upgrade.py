from tools import configs
from tools.configs import path_define
from tools.services import upgrade_service


def main():
    upgrade_service.upgrade_ark_pixel()

    for upgrade_config in configs.upgrade_configs:
        upgrade_service.upgrade_fonts(upgrade_config)

    for parent_dir, dir_names, file_names in path_define.fonts_dir.walk():
        for file_name in file_names:
            if not file_name.endswith('.txt'):
                continue
            file_path = parent_dir.joinpath(file_name)
            text = file_path.read_text('utf-8')
            file_path.write_text(text, 'utf-8')


if __name__ == '__main__':
    main()
