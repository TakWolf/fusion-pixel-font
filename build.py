import logging

import configs
from configs import path_define
from services import dump_service, design_service, font_service, info_service, publish_service, image_service, template_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    for dump_config in configs.dump_configs:
        dump_service.dump_font(dump_config)

    for width_mode in configs.width_modes:
        alphabet, glyph_file_paths, fallback_infos = design_service.collect_glyph_files(width_mode)
        font_service.make_fonts(width_mode, alphabet, glyph_file_paths)
        info_service.make_info_file(width_mode, alphabet, fallback_infos)
        info_service.make_alphabet_txt_file(width_mode, alphabet)
        publish_service.make_release_zips(width_mode)
        template_service.make_alphabet_html_file(width_mode, alphabet)
    image_service.make_preview_image_file()
    template_service.make_index_html_file()


if __name__ == '__main__':
    main()
