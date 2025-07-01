from tools.configs import options
from tools.services import font_service, update_service, check_service


def main():
    update_service.setup_ark_pixel_glyphs()

    mappings = font_service.load_mappings()
    for font_size in options.font_sizes:
        check_service.check_glyph_files(font_size, mappings)


if __name__ == '__main__':
    main()
