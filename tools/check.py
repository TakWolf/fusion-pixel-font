from tools.configs import options
from tools.services import upgrade_service, font_service, check_service


def main():
    upgrade_service.setup_ark_pixel()

    mappings = font_service.load_mappings()
    for font_size in options.font_sizes:
        check_service.check_glyph_files(font_size, mappings)


if __name__ == '__main__':
    main()
