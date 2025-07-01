from tools import configs
from tools.services import update_service


def main():
    update_service.update_ark_pixel_glyphs_version()
    update_service.setup_ark_pixel_glyphs()

    for update_config in configs.update_configs:
        update_service.update_fonts(update_config)


if __name__ == '__main__':
    main()
