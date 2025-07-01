from pixel_font_knife import glyph_mapping_util

from tools import configs
from tools.configs import options
from tools.services import update_service, check_service


def main():
    update_service.setup_ark_pixel_glyphs()

    mappings = [glyph_mapping_util.load_mapping(file_path) for file_path in configs.mapping_file_paths]
    for font_size in options.font_sizes:
        check_service.check_glyph_files(font_size, mappings)


if __name__ == '__main__':
    main()
